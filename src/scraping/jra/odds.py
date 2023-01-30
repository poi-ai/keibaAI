import babaid
import datetime
import jst
import line
import log
import output
import pandas as pd
import pd_read
import re
import requests
import time
import traceback
from bs4 import BeautifulSoup
from base import Base

class Odds(Base):
    '''中央競馬オッズ取得クラス

    Class Parameter:
       ODDS_URL(str) : JRAのオッズ関連ページの共通URL
       RACE_CARD_URL(str) : JRAの出馬表関連ページの共通URL

    Instance Parameter:
       odds_param(list<str>) : 各競馬場のレース一覧ページ(オッズ)のPOSTパラメータ
       info_param(list<str>) : 各競馬場のレース一覧ページ(出馬表)のPOSTパラメータ
       race_info(list<RaceInfo>) : 各レース情報を持つリスト
       next_get_time(datetime) : 次回オッズ取得時刻
       write_data(DataFrame) : 出力まで一時保存するオッズデータ
       kaisai(bool) : レース開催があるか
    '''
    # オッズ関連ページのURL
    ODDS_URL = 'https://www.jra.go.jp/JRADB/accessO.html'
    # 出馬表関連ページのURL
    RACE_CARD_URL = 'https://www.jra.go.jp/JRADB/accessD.html'

    def __init__(self):
        super().__init__()
        self.logger.info('----------------------------')
        self.logger.info('中央競馬オッズ記録システム起動')
        line.send('中央競馬オッズ記録システム起動')
        self.logger.info('初期処理開始')
        self.odds_param = []
        self.info_param = []
        self.race_info = []
        self.next_get_time = 0
        self.write_data = pd.DataFrame(columns = ['レースID','馬番', '単勝オッズ', '複勝下限オッズ', '複勝上限オッズ', '記録時刻', '発走まで', 'JRAフラグ'])
        if self.get_param('odds'):
            self.kaisai = True
            self.get_param('info')
            self.get_race_info(True)
            self.logger.info(f'初期処理終了 開催場数：{len(self.odds_param)} 記録対象レース数：{len(self.race_info)}')
        else:
            self.kaisai = False

    def do_action(self, cname, sleep_time = 0, retry_count = 3):
        '''POSTリクエストを送り、HTML情報を受け取る

        Args:
            cname(str):POSTパラメータ

        Returns:
            soup(bs4.BeautifulSoup):受け取ったHTML
        '''
        for _ in range(retry_count):
            try:
                r = requests.post(self.ODDS_URL, data = {'cname':cname})
                r.encoding = r.apparent_encoding
                soup = BeautifulSoup(r.text, 'lxml')
            except Exception as e:
                self.logger.error(e)
                self.logger.error(traceback.format_exc())
                self.logger.error(f'レスポンスコード：{str(r.status_code)}')
                if sleep_time != 0:
                  time.sleep(sleep_time)
            else:
                return soup
        else:
            return -1

    def extract_param(self, html):
        '''HTMLからdoActionの第二引数を抽出する

        Args:
            html(strに変換可能な型):抽出元のHTMLコード

        Returns:
            param(list<str>):抽出した第二引数のリスト
        '''
        param = [m.group(1) for m in re.finditer('access.\.html\', \'(\w+/\w+)', str(html))]

        return param

    def get_param(self, page_type):
        '''稼働日の各競馬場のレースリストページのパラメータを取得する

        Args:
            page_type(str):サイトの種類
                           odds:オッズページ,info:出馬表ページ
        '''
        # 今週の開催一覧ページのHTMLを取得
        if page_type == 'odds':
            soup = self.do_action('pw15oli00/6D')
            self.logger.info('開催情報取得')
        else:
            soup = self.do_action('pw01dli00/F3')
            self.logger.info('レース発走情報取得')

        # 開催情報のリンクがある場所を切り出し
        kaisai_frame = soup.find('div', id = 'main')

        # HTML内から日付を取得
        soup = BeautifulSoup(str(kaisai_frame), 'lxml')
        kaisai_dates = soup.find_all('h3')

        for i, kaisai_date in enumerate(kaisai_dates):
            # レース日と稼働日が一致する枠の番号を取得
            m = re.search(r'(\d+)月(\d+)日', str(kaisai_date))
            '''TODO 動作確認後に削除
            ・レース開催日 if jst.month() == m.group(1) and jst.day() == m.group(2):
            ・月～水曜日 if '直近レース開催の月' == m.group(1) and '直近レース開催の日' == m.group(2):
            ・木～金曜日 動作確認不可(JRAの今週の開催ページに出走表へのリンクがないため)
            '''
            if jst.month() == m.group(1) and jst.day() == m.group(2):
                # 合致した枠内のHTMLを取得
                links = BeautifulSoup(str(soup.find_all('div', class_='link_list multi div3 center')[i]), 'lxml')
                # パラメータを抽出しインスタンス変数に格納
                if page_type == 'odds':
                    self.odds_param = self.extract_param(links)
                else:
                    self.info_param = self.extract_param(links)
                time.sleep(3)
                return True

        # 開催がない場合
        return False

    def get_race_info(self, init_flg = False):
        '''レース情報を取得

        Args:
            init_flg(bool) : 初期処理(インスタンス作成)か主処理(インスタンス更新)か
                             T:初期処理,F:主処理
        '''
        today_race_time = []

        # 発走時刻の切り出し
        for param in self.info_param:

            baba_race_time = []
            soup = self.do_action(param)
            if soup == -1:
                self.logger.error(f'{babaid.jra(param[9:11])}競馬場のレーステーブルの取得に失敗')
                # 初期処理で失敗した場合のみエラーとして処理
                if init_flg:
                    raise
                else:
                    self.logger.info(f'{babaid.jra(param[9:11])}競馬場の発走時刻更新を行いません')
                    time.sleep(3)
                    continue

            # HTMLからレース情報記載のテーブル箇所のみDataFrameに切り出し
            info_table = pd_read.html(str(soup))[0]

            # カラムが正常に取れているかのチェック
            if not '発走時刻' in info_table.columns:
                self.logger.warning(f'{babaid.jra(param[9:11])}競馬場のレーステーブルの正常データ取得に失敗')

                if init_flg:
                    raise
                else:
                    self.logger.info(f'{babaid.jra(param[9:11])}競馬場の発走時刻更新を行いません')
                    time.sleep(3)
                    continue

            for i in info_table['発走時刻']:
                m = re.search(r'(\d+)時(\d+)分', i)
                baba_race_time.append(datetime.datetime(int(jst.year()), int(jst.month()), int(jst.day()), int(m.group(1)), int(m.group(2)), 0))

            today_race_time.append(baba_race_time)

            time.sleep(2)

        # レース情報の取得
        for kaisai_num, list_param in enumerate(self.odds_param):
            soup = self.do_action(list_param)
            if soup == -1:
                self.logger.error(f'オッズ一覧の取得に失敗しました')
                raise

            # 単勝・複勝オッズページのパラメータを取得
            tanpuku = [self.extract_param(str(i))[0] for i in soup.find_all('div', class_='tanpuku')]

            ######## MEMO #######
            # find_allの第二引数を↓に書き換えれば、別の馬券のパラメータも取得できる
            # wakuren,umaren,wide,umatan,trio,tierce
            #####################

            for race_num, param in enumerate(tanpuku):
                if init_flg:
                    # 初期処理の場合はレース情報をRaceInfo型で保存する
                    try:
                        self.race_info.append(RaceInfo(param, param[9:11], param[19:21], today_race_time[kaisai_num][race_num]))
                    except Exception as e:
                        self.error_output(f'{babaid.jra(param[9:11])}競馬場の発走時刻追加の初期処理に失敗しました', e, traceback.format_exc())
                        raise
                else:
                    # 主処理の場合は発走時間が更新されているかのチェック
                    try:
                        for race in self.race_info:
                            if race.baba_code == param[9:11] and race.race_no == param[19:21]:
                                if race.race_time != today_race_time[kaisai_num][race_num]:
                                    self.logger.info(f'発走時間変更 {babaid.jra(race.baba_code)}{race.race_no}R {jst.clock(race.race_time)}→{jst.clock(today_race_time[kaisai_num][race_num])}')
                                    race.race_time = today_race_time[kaisai_num][race_num]
                    except Exception as e:
                        self.error_output(f'{babaid.jra(param[9:11])}競馬場の発走時刻追加処理に失敗しました', e, traceback.format_exc())
                        self.logger.info(f'{babaid.jra(param[9:11])}競馬場のレーステーブルの発走時刻更新を行いません')
                        time.sleep(3)
                        continue

    def time_check(self, called = False):
        '''次のオッズ記録時間までの秒数を計算する
        Args:
            called(bool):別処理が同時に走っているか

        Returns:
            time_left(int):次の取得までの秒数(called = True時)
            flg(bool):待機時間後に次のオッズ取得時間か(called = Flase時)
        '''

        # 23時～8時に動いていたら異常とみなし強制終了
        if int(jst.hour()) <= 8 or 23 == int(jst.hour()):
            self.logger.info('取得時間外に起動しているため強制終了します')
            line.send('取得時間外に起動しているため強制終了します')
            exit()

        self.logger.info('オッズ記録時間チェック処理開始')
        # 現在時刻取得
        NOW = jst.now()
        # 次のx時x分00秒
        NEXT_MINITURES = NOW + datetime.timedelta(seconds = 60 - int(jst.second()))

        # 次の取得時間をリセット
        self.next_get_time = NOW + datetime.timedelta(days = 1)

        # 各レース毎に次のx分00秒が記録対象かチェック
        for race in self.race_info:

            # 最終出力待ちか記録済以外の場合
            if race.record_flg != '4' and race.record_flg != '-1':
                # 次のx分00秒からレース発走までの時間
                time_left = int((race.race_time - NEXT_MINITURES).total_seconds())

                # 発走12分よりも前の場合
                if time_left > 720:
                    self.next_get_time = jst.time_min(self.next_get_time, race.race_time - datetime.timedelta(seconds = 720))
                # 発走12分前から1分以内の場合
                elif time_left >= 59:
                    self.next_get_time = NEXT_MINITURES
                # 発走1分前から発走後20分以内の場合
                elif time_left > -1200:
                    self.next_get_time = jst.time_min(self.next_get_time, race.race_time + datetime.timedelta(seconds = 1200))
                # 発走後20分以降の場合
                else:
                    self.next_get_time = NEXT_MINITURES

        # 次の記録時間までの時間(秒)
        time_left = int((self.next_get_time - jst.now()).total_seconds())

        # 出力待ちのみの場合はノータイムで出力するように
        if self.wait_check(): time_left = 0

        # 別処理と同時起動の場合は待機せず時間を返す
        if called:
            return time_left
        else:
            # 取得対象レースを抽出
            self.get_target_race(self.next_get_time)

            self.logger.info(f'次の記録時間まで{time_left}秒')

            # 11分以上なら10分後に発走時刻再チェック
            if time_left > 660:
                time.sleep(600)
                return False
            elif time_left > 1:
                time.sleep(time_left + 1)
                return True
            else:
                return True


    def get_target_race(self, get_time):
        '''待機時間後に取得対象となるレースを抽出'''

        for race in self.race_info:
            # 最終出力待ちか記録済以外の場合
            if race.record_flg != '4' and race.record_flg != '-1':
                # 次の記録時間とレース発走の時間差
                diff_time = int((race.race_time - get_time).total_seconds())

                # 発走12分前から1分以内の場合
                if 720 >= diff_time >= 59:
                    race.record_flg = '1'
                # 発走後20分以降の場合
                elif -1200 >= diff_time:
                    race.record_flg = '2'

    def continue_check(self):
        '''処理を続ける(=全レース記録済みでない)かのチェックを行う'''
        for race in self.race_info:
            if race.record_flg != '-1':
                return True
        return False

    def wait_check(self):
        '''全レース出力待ちかのチェックを行う'''
        for race in self.race_info:
            if race.record_flg != '4':
                return False
        return True

    def get_select_realtime(self):
        '''暫定オッズ取得対象レースの抽出'''

        # 取得回数記録
        get_count = 0

        # 暫定オッズを取得
        for race in self.race_info:
            if race.record_flg == '1':
                try:
                    self.get_odds(race)
                except Exception as e:
                    self.error_output(f'{babaid.jra(race.baba_code)}{race.race_no}Rの暫定オッズ取得処理でエラー', e, traceback.format_exc())
                    race.record_flg = '0'
                    continue
                race.record_flg = '3'
                get_count += 1

            # アクセス過多防止のため、5レース取得ごとに1秒待機(バグリカバリ)
            if get_count % 5 == 0 and get_count != 0:
                time.sleep(1)

    def get_select_confirm(self):
        '''最終オッズ取得対象レースの抽出'''

        for race in self.race_info:
            if race.record_flg == '2':
                try:
                    self.get_odds(race)
                except Exception as e:
                    self.error_output(f'{babaid.jra(race.baba_code)}{race.race_no}Rの確定オッズ取得処理でエラー', e, traceback.format_exc())
                    race.record_flg = '-1'
                    continue
                race.record_flg = '4'
                time.sleep(3)

            # x分40秒を超えたら取得を後回しに
            if int(jst.second()) > 40:
                break

    def get_odds(self, race, count = 1):
        '''(単勝・複勝)オッズの取得・記録を行う'''
        # オッズのテーブルを取得
        self.logger.info(str(race.race_param))
        soup = self.do_action(race.race_param)
        if soup == -1:
            self.logger.error(f'オッズの取得に失敗しました')
            raise
        odds_table = pd_read.html(str(soup))[0]

        try:
            # 馬番・単勝オッズのカラムのみ抽出
            odds_data = odds_table.loc[:, ['馬番', '単勝']]
            # 複勝オッズのカラムを下限と上限に別々のカラムに分割(レースによってカラム名が変わるため位置で指定)
            fukusho = odds_table[odds_table.columns[4]].str.split('-', expand = True)
        except:
            if count < 5:
                self.logger.warning(f'オッズ取得処理で正常なデータが取得できませんでした。({count}回目)')
                self.logger.warning('再度オッズ取得処理を実行します。')
                self.get_odds(race, count + 1)
                return
            else:
                self.logger.error('オッズ取得処理で5度正常なデータが取得できませんでした')
                self.logger.info('-----------------')
                self.logger.info(str(soup))
                self.logger.info('-----------------')
                self.logger.info(odds_table)
                self.logger.info('-----------------')
                logger
                raise

        self.logger.info(f'{babaid.jra(race.baba_code)}{race.race_no}Rの{str(round((race.race_time - jst.now()).total_seconds() / 60)) + "分前" if race.record_flg == "1" else "最終"}オッズ取得')

        # 最左列にレースIDのカラム追加
        odds_data.insert(0, 'race_id', jst.date() + race.baba_code.zfill(2) + race.race_no.zfill(2))
        # 最右列に現在時刻(yyyyMMddHHMM)・発走までの残り時間(分)・JRAフラグの追加
        odds_data = pd.concat([odds_data, fukusho, pd.DataFrame([[jst.mtime(), max(-1, int((race.race_time - jst.now()).total_seconds() / 60)), race.jra_flg] for _ in range(len(odds_data))], index = odds_data.index)], axis = 1)
        odds_data.set_axis(self.write_data.columns, axis = 1, inplace = True)
        # 一時保存用変数に格納
        self.write_data = pd.concat([odds_data, self.write_data])

    def record_odds(self):
        '''取得したオッズをCSV/Google Spread Sheetに出力する'''

        # CSVに出力する
        try:
            output.csv(self.write_data, f'jra_resultodds_{jst.year()}{jst.zmonth()}')
        except Exception as e:
            self.error_output('オッズ出力処理でエラー', e, traceback.format_exc())

        # TODO Google Spread Sheetに出力
        # writesheet.write_spread_sheet(self.write_data, jst.month().zfill(2))

        # 記録用データを空にする
        self.write_data = self.write_data[:0]

        # 出力待ちのフラグを変更する
        for race in self.race_info:
            # 暫定オッズフラグの変更
            if race.record_flg == '3':
                race.record_flg = '0'
            # 最終オッズフラグの変更
            if race.record_flg == '4':
                race.record_flg = '-1'

        self.logger.info('オッズデータをCSVへ出力')

    def error_output(self, message, e, stacktrace):
        '''エラー時のログ出力/LINE通知を行う

        Args:
            message(str) : エラーメッセージ
            e(str) : エラー名
            stacktrace(str) : スタックトレース
        '''
        self.logger.error(message)
        self.logger.error(e)
        self.logger.error(stacktrace)
        line.send(message)
        line.send(e)
        line.send(stacktrace)

class RaceInfo():
    '''各レースの情報を保持を行う
    Instance Parameter:
       race_param(str) : オッズページのPOSTパラメータ
       baba_code(str) : 競馬場コード
       race_no(str) : レース番号,xxRのxxの部分
       race_time(datetime) : 発走時刻
       record_flg(str) : 0,記録時刻待ち
                         1,暫定オッズ取得待ち
                         2,最終オッズ取得待ち
                         3,暫定オッズ出力待ち
                         4,最終オッズ出力待ち
                         -1,最終オッズ出力済
       jra_flg(str) : 1,中央 0,地方
    '''

    def __init__(self, race_param, baba_code, race_no, race_time):
        self.race_param = race_param
        self.baba_code = baba_code
        self.race_no = race_no
        self.race_time = race_time
        self.record_flg = '0'
        self.jra_flg = '1'

# 単体起動時
if __name__ == '__main__':
    # ログ用インスタンス作成
    logger = log.Logger()

    # 中央競馬用インスタンス作成
    try:
        jra = Odds()
    except Exception as e:
        logger.error('初期処理でエラー')
        logger.error(e)
        logger.error(traceback.format_exc())
        line.send('初期処理でエラー')
        line.send(e)
        line.send(traceback.format_exc())
        exit()

    if not jra.kaisai:
        logger.info('本日行われるレースはありません')
        exit()

    while True:
        # 全レース記録済かチェック
        if not jra.continue_check():
            break

        while True:

            # 発走時刻更新
            try:
                jra.get_race_info()
            except Exception as e:
                jra.error_output('発走時刻更新処理でエラー', e, traceback.format_exc())
                exit()

            # 発走までの時間チェック待機
            try:
                if jra.time_check():
                    break
            except Exception as e:
                jra.error_output('発走時刻までの待機処理でエラー', e, traceback.format_exc())
                exit()

        # 暫定オッズ取得処理
        jra.get_select_realtime()

        time.sleep(2)

        # 確定オッズ取得処理
        jra.get_select_confirm()

        # 記録データが格納されていてx分40秒を過ぎていなければCSV出力
        if int(jst.second()) <= 40 and len(jra.write_data) != 0:
            jra.record_odds()

    logger.info('中央競馬オッズ記録システム終了')
    line.send('中央競馬オッズ記録システム終了')