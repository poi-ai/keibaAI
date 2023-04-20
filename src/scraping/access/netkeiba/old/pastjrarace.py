import csv
import itertools
import os
import package
import pastjraracedata
import sys
import time
import traceback
import re
from common import logger, jst, soup as Soup, line, validate
from tqdm import tqdm

class RaceData():
    '''netkeibaのサイトから中央競馬の過去レースデータを取得する
    Instance Parameter:
        latest_date(str) : 取得対象の最も新しい日付(yyyyMMdd)
                          デフォルト : システム稼働日前日
        oldest_date(str) : 取得対象の最も古い日付(yyyyMMdd)
                          デフォルト : 20070728(閲覧可能な最古の日付)
        date(list<str>) : 取得対象の日付(yyyyMMdd)
        recorded_horse_id(list<str>) : 記録済みの競走馬ID
        output_type(str) : 出力ファイルを分割
                           m : 月ごと(デフォルト)、y : 年ごと、a : 全ファイルまとめて
    '''

    def __init__(self, oldest_date = '20070728', latest_date = jst.yesterday(), output_type = 'm'):
        logger.info('----------------------------')
        logger.info('中央競馬過去レースデータ取得システム起動')
        logger.info('初期処理開始')
        self.__oldest_date, self.__latest_date = validate.check('20070728', oldest_date, latest_date)
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
        hold_date_list = self.get_hold_date()

        logger.info(f'取得対象日数は{len(hold_date_list)}日です')
        print(f'取得対象日数は{len(hold_date_list)}日です')

        # レースのある日を1日ずつ遡って取得処理を行う
        for hold_date in tqdm(hold_date_list):

            logger.info(f'{jst.change_format(hold_date, "%Y%m%d", "%Y/%m/%d")}のレースデータの取得を開始します')

            # 指定日に行われる全レースのレースID取得
            try:
                race_id_list = self.get_race_id(hold_date)
            except Exception as e:
                self.error_output('レースURL取得処理でエラー', e, traceback.format_exc())
                continue

            logger.info(f'取得レース数：{len(race_id_list)}')

            # レースIDからレース情報を取得する
            for race_id in race_id_list:
                race_data = pastjraracedata.GetRaceData(race_id, self.output_type)
                self.recorded_horse_id = race_data.main(self.recorded_horse_id)

            time.sleep(3)

    def get_hold_date(self):
        '''取得対象範囲内でのレース開催日を取得

        Returns:
            date_list(list[str]): レース開催日をyyyyMMdd型で持つリスト

        '''

        # 取得対象の最古/最新日付の年と月を抽出
        target_year = self.latest_date[:4]
        target_month = self.latest_date[4:6]
        latest_year = self.latest_date[:4]
        latest_month = self.latest_date[4:6]
        oldest_year = self.oldest_date[:4]
        oldest_month = self.oldest_date[4:6]

        # 開催日を格納するリスト
        date_list = []

        for _ in tqdm(range((int(target_year) - int(oldest_year)) * 12  + int(target_month) - int(oldest_month) + 1)):
            # 開催月を取得
            hold_list = self.get_month_hold_date(target_year, target_month)
            hold_list.sort(reverse = True)

            # 開始日と同月の場合、開催日以前の日の切り落とし
            if target_year == latest_year and target_month == latest_month:
                hold_list.append(self.latest_date)
                hold_list.sort(reverse = True)
                hold_list = hold_list[hold_list.index(self.latest_date) + 1:]

            # 終了日と同月の場合、開催日以降の日の切り落とし
            if target_year == oldest_year and target_month == oldest_month:
                hold_list.append(self.oldest_date)
                hold_list.sort(reverse = True)
                if hold_list.count(self.oldest_date) == 2:
                    hold_list = hold_list[:hold_list.index(self.oldest_date) + 1]
                else:
                    hold_list = hold_list[:hold_list.index(self.oldest_date)]

            # 開催日を格納
            date_list.append(hold_list)

            # 前月へ
            if target_month == '01':
                target_year = str(int(target_year) - 1)
                target_month = '12'
            else:
                target_month = str(int(target_month) - 1).zfill(2)

        return list(itertools.chain.from_iterable(date_list))

    def get_month_hold_date(self, years, month):
        '''指定した年月の中央競馬の開催日を取得

        Args:
            years(str):取得する対象の年。yyyy
            month(str):取得する対象の月。MM

        Return:
            hold_list(list):対象年月の開催日。要素はyyyyMMdd形式のstr型。

        '''
        # 開催カレンダーページからリンクを取得
        soup = Soup.get_soup(f'https://race.netkeiba.com/top/calendar.html?year={years}&month={month}')
        links = soup.find_all('a')
        hold_list = []
        for link in links:
            date_url = link.get('href')
            # カレンダー内にあるリンク(=レースがある日)だけ取得
            # 2007年と2008年以降でリンク先が異なるので取得ロジック修正
            if int(years) == 2007:
                rematch = re.search('race/sum/(\d+)/(\d+)', str(link))
                if rematch != None:
                    hold_list.append(rematch.groups()[1])
            elif int(years) > 2007:
                if 'kaisai_date' in date_url:
                    hold_list.append(date_url[len(date_url) - 8:])

        return list(set(hold_list))

    def get_race_id(self, hold_date):
        '''対象年月日のレース番号を取得

        Args:
            hold_date(list):中央競馬開催日の年月日(yyyyMMdd)

        Returns:
            race_id_list(list):対象年月日のレースIDを要素に持つリスト

        '''
        # 各開催日からレースIDをリストに代入
        race_id_list = []

        # ページ内の全URL取得
        cource_url = f'https://race.netkeiba.com/top/race_list_sub.html?kaisai_date={hold_date}'

        soup = Soup.get_soup(cource_url)
        links = soup.find_all('a')

        for link in links:
            race_url = link.get('href')
            # レース結果ページのみ取得しその中からレースIDを切り出す
            if 'result' in race_url:
                race_id_list.append(race_url[28:40])

        return race_id_list

    def get_recorded_horse(self):
        '''CSVから記録済みの競走馬IDを記録する'''

        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'csv', 'jra_horse_char_info.csv')

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

    logger.info('中央競馬過去レースデータ取得システム終了')
    line.send('中央競馬過去レースデータ取得システム終了')
