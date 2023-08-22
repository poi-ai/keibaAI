import csv
import itertools
import package
import pastnarracedata
import os
import sys
import time
import traceback
from common import logger, jst, soup as Soup, line, validate, wordchange
from datetime import datetime, timedelta
from tqdm import tqdm

class RaceData():
    '''netkeibaのサイトから地方競馬の過去レースデータを取得する
    Instance Parameter:
        latest_date(str) : 取得対象の最も新しい日付(yyyyMMdd)
                          デフォルト : システム稼働日前日
        oldest_date(str) : 取得対象の最も古い日付(yyyyMMdd)
                          デフォルト : 20150225(閲覧可能な最古の日付)
        date(list<str>) : 取得対象の日付(yyyyMMdd)
        recorded_horse_id(list<str>) : 記録済みの競走馬ID
        output_type(str) : 出力ファイルを分割
                           m : 月ごと(デフォルト)、y : 年ごと、a : 全ファイルまとめて
    '''

    def __init__(self, oldest_date = '20150225', latest_date = jst.yesterday(), output_type = 'm'):
        logger.info('----------------------------')
        logger.info('地方競馬過去レースデータ取得システム起動')
        logger.info('初期処理開始')
        self.__oldest_date, self.__latest_date = validate.check('20150225', oldest_date, latest_date)
        logger.info('日付のバリデーションチェック終了')
        self.__recorded_horse_id = []
        self.__output_type = output_type

    @property
    def latest_date(self): return self.__latest_date
    @property
    def oldest_date(self): return self.__oldest_date
    @property
    def recorded_horse_id(self): return self.__recorded_horse_id
    @property
    def output_type(self): return self.__output_type
    @latest_date.setter
    def latest_date(self, latest_date): self.__latest_date = latest_date
    @oldest_date.setter
    def oldest_date(self, oldest_date): self.__oldest_date = oldest_date
    @recorded_horse_id.setter
    def recorded_horse_id(self, recorded_horse_id): self.__recorded_horse_id = recorded_horse_id
    @output_type.setter
    def output_type(self, output_type): self.__output_type = output_type

    def main(self):
        '''主処理、各メソッドの呼び出し'''

        # CSVから既に記録済みの競走馬IDを取得
        try:
            self.get_recorded_horse()
        except Exception as e:
            self.error_output('記録済み競走馬データCSV取得処理でエラー', e, traceback.format_exc())
            return

        # 対象の日付リストの取得
        date_list = self.get_between_date()

        logger.info(f'取得対象日数は{len(date_list)}日です')
        print(f'取得対象日数は{len(date_list)}日です')

        # 1日ずつ遡って取得処理を行う
        for date in tqdm(date_list):

            logger.info(f'{jst.change_format(date, "%Y%m%d", "%Y/%m/%d")}のレースデータの取得を開始します')

            # 日付から各競馬場の開催IDを取得
            try:
                hold_id_list = self.get_hold_id(date)
            except Exception as e:
                self.error_output('開催ID取得処理でエラー', e, traceback.format_exc())
                continue

            # レースIDを保管
            race_id_list = []

            # 開催IDからレースIDを取得
            for hold_id in hold_id_list:
                # 指定日に行われる全レースのレースIDの取得
                try:
                    race_id_list = self.get_race_id(date, hold_id)
                except Exception as e:
                    self.error_output('レースURL取得処理でエラー', e, traceback.format_exc())
                    continue

            # レースIDからレース情報を取得する
            for race_id in race_id_list:
                race_data = pastnarracedata.GetRaceData(wordchange.rm(race_id), self.output_type)
                self.recorded_horse_id = race_data.main(self.recorded_horse_id)
                
                print(self.recorded_horse_id)

            time.sleep(3)

    def get_between_date(self):
        '''取得対象間の全日付を取得する

        Return:
            target_date_list(list[str]):
                oldest_dateからlatest_date間の全日付のリスト(yyyyMMdd型)
        '''

        # 対象日格納用
        target_date_list = []

        target_date = datetime.strptime(self.latest_date, '%Y%m%d')
        end_date = datetime.strptime(self.oldest_date, '%Y%m%d')

        while True:
            if target_date < end_date:
                break
            target_date_list.append(datetime.strftime(target_date, '%Y%m%d'))
            target_date = target_date - timedelta(days = 1)

        return target_date_list

    def get_hold_id(self, kaisai_date):
        '''指定日に開催された各競馬場の開催IDを取得する

        Args:
            kaisai_date(str):取得したい日付(yyyyMMddフォーマット)

        Returns:
            kaisai_id_list(list[str]):指定日にされた各競馬場の開催IDのリスト
        '''
        # 開催IDが記載されているURL
        url = f'https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date={kaisai_date}'

        kaisai_id_list = []

        soup = Soup.get_soup(url)
        # 開催IDのリンクはli属性内にあるのでliを取得
        li = soup.find_all('li')

        # li属性内のa属性を取得
        links = [link.find_all('a') for link in li]

        # 一元化
        links = list(itertools.chain.from_iterable(links))

        # a属性から開催IDのリンクがあるURLを抽出
        for link in links:
            hold_url = link.get('href')
            # レース結果ページのみ取得しその中からレースIDを切り出す
            if 'kaisai_id' in hold_url:
                kaisai_id_list.append(hold_url[11:21])

        return kaisai_id_list

    def get_race_id(self, kaisai_date, kaisai_id):
        '''指定した開催IDからレースIDを取得する

        Args:
            kaisai_date(str):開催日(yyyyMMddフォーマット)
            kaisai_id(str):開催ID(netkeibaの独自フォーマット)

        Returns:
            race_id_list(list[str]):レースID(netkeiba独自)のリスト
        '''
        # 開催IDが記載されているURL
        url = f'https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date={kaisai_date}&kaisai_id={kaisai_id}'

        race_id_list = []

        soup = Soup.get_soup(url)
        li = soup.find_all('li')

        # li属性内のa属性を取得
        links = [link.find_all('a') for link in li]

        # 一元化
        links = list(itertools.chain.from_iterable(links))

        # a属性から開催IDのリンクがあるURLを抽出
        for link in links:
            race_url = link.get('href')
            # レース結果ページのみ取得しその中からレースIDを切り出す
            if 'result.html' in race_url:
                race_id_list.append(race_url[28:40])

        return race_id_list

    def get_recorded_horse(self):
        '''CSVから記録済みの競走馬IDを記録する'''

        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'csv', 'nar_horse_char_info.csv')

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)

                self.recorded_horse_id = [row[0] for row in reader]
        except FileNotFoundError:
            return []

    def error_output(self, message, e, stacktrace):
        '''エラー時のログ出力/LINE通知を行う
        Args:
            message(str) : エラーメッセージ
            e(str) : エラー名
            stacktrace(str) : スタックトレース
        '''
        logger.error(message)
        logger.error(e)
        logger.error(stacktrace)
        line.send(message)
        line.send(e)
        line.send(stacktrace)

if __name__ == '__main__':
    # ログ用インスタンス作成
    # プログレスバーを出すためコンソールには出力しない
    logger = logger.Logger(0)

    # 初期処理
    try:
        if len(sys.argv) >= 4:
            rd = RaceData(sys.argv[1], sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 3:
            rd = RaceData(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 2:
            rd = RaceData(sys.argv[1])
        else:
            rd = RaceData()
    except Exception as e:
        logger.error('初期処理でエラー')
        logger.error(e)
        logger.error(traceback.format_exc())
        line.send('初期処理でエラー')
        line.send(e)
        line.send(traceback.format_exc())
        raise

    # 主処理
    rd.main()

    logger.info('地方競馬過去レースデータ取得システム終了')
    line.send('地方競馬過去レースデータ取得システム終了')
