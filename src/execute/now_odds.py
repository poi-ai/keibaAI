import config
import jst
import line
import time
import traceback
from execbase import ExecBase

class NowOdds(ExecBase):
    '''中央・地方競馬オッズ取得
    Instance Parameter:
       jra_flg(bool) : 中央競馬処理稼働フラグ
       nar_flg(bool) : 地方競馬処理稼働フラグ
    '''
    def __init__(self):
        super().__init__()
        # 取得対象設定
        if config.ASSOSIATION == '1':
            self.jra_flg = self.nar_flg = True
        elif config.ASSOSIATION == 'JRA':
            self.jra_flg = True
            self.nar_flg = False
        elif config.ASSOSIATION == 'NAR':
            self.jra_flg = True
            self.nar_flg = False
        else:
            self.error_output(f'中央・地方競馬オッズ取得システム取得対象設定値エラー：{config.ASSOSIATION}')
            exit()

        self.logger.info('----------------------------')
        self.logger.info('中央・地方競馬オッズ記録システム起動')
        self.logger.info('初期処理開始')
        line.send('中央・地方競馬オッズ記録システム起動')
        self.jra, self.nar = self.create_instance()
        self.logger.info('初期処理終了')
        self.main()
        self.logger.info('中央・地方競馬オッズ記録システム終了')
        line.send('中央・地方競馬オッズ記録システム終了')

    def main(self):
        '''主処理'''
        while True:
            # 全レース記録済みかのチェック
            self.continue_check()

            # 中央・地方ともに記録済みなら処理終了
            if not (self.jra_flg or self.nar_flg):
                self.logger.info('中央・地方競馬オッズ記録システム終了')
                return

            while True:
                # 発走時刻更新処理
                self.get_race_info()

                # 時間チェック/待機処理
                if self.time_check():
                    break

            # オッズ取得処理
            self.get_select()

            # CSV出力処理
            self.record_odds()

    def create_instance(self):
        '''インスタンスの生成を行う'''

        # 中央競馬用インスタンス作成
        try:
            jra_odds = self.access.jra.odds
        except Exception as e:
            self.error_output('中央_初期処理でエラー', e, traceback.format_exc(), False)
            self.jra_flg = False

        if not jra_odds.kaisai:
            self.logger.info('中央_本日の開催はありません')
            self.jra_flg = False

        # 地方競馬用インスタンス作成
        try:
            nar_odds = self.access.keibago.odds
        except Exception as e:
            self.error_output('地方_初期処理でエラー', e, traceback.format_exc(), False)
            self.nar_flg = False

        return jra_odds, nar_odds

    def continue_check(self):
        '''処理を続けるか(=全レース記録済みでないか)のチェックを行う'''

        # 中央が全レース記録済かチェック
        if self.jra_flg:
            self.jra_flg = self.jra.continue_check()

        # 地方が全レース記録済かチェック
        if self.nar_flg:
            self.nar_flg = self.nar.continue_check()

    def get_race_info(self):
        '''発走時刻に変更があった場合に更新を行う'''

        # 中央発走時刻更新
        if self.jra_flg:
            try:
                self.jra.get_race_info()
            except Exception as e:
                self.error_output('中央_発走時刻更新処理でエラー', e, traceback.format_exc(), False)
                self.jra_flg = False

        # 地方発走時刻更新
        if self.nar_flg:
            try:
                self.nar.get_race_info()
            except Exception as e:
                self.error_output('地方_発走時刻更新処理でエラー', e, traceback.format_exc(), False)
                self.nar_flg = False

    def time_check(self):
        '''記録時間までの時間を取得し、待機する'''
        jra_wait_time = 99999999
        nar_wait_time = 99999999

        # 中央の発走までの時間チェック
        if self.jra_flg:
            try:
                jra_wait_time =  self.jra.time_check(True)
                self.logger.info(f'中央：次の記録時間まで{jra_wait_time}秒')
            except Exception as e:
                self.error_output('中央_待機時間チェック処理でエラー', e, traceback.format_exc(), False)
                self.jra_flg = False
        else:
            self.logger.info(f'中央の取得対象レースはありません')

        # 地方の発走までの時間チェック
        if self.nar_flg:
            try:
                nar_wait_time = self.nar.time_check(True)
                self.logger.info(f'地方：次の記録時間まで{nar_wait_time}秒')
            except Exception as e:
                self.error_output('地方_時刻までの待機時間チェック処理でエラー', e, traceback.format_exc(), False)
                self.nar_flg = False
        else:
            self.logger.info(f'地方の取得対象レースはありません')

        # 0の場合は取得処理はすべて終了して出力待ちの状態なので、もう一方の待機時間に合わせる
        if jra_wait_time == 0 and nar_wait_time != 0:
            time_left = nar_wait_time
            # NARの取得対象レースのフラグ切り替え
            self.nar.get_target_race(self.nar.next_get_time)
        elif jra_wait_time != 0 and nar_wait_time == 0:
            time_left = jra_wait_time
            # JRAの取得対象レースのフラグ切り替え
            self.nar.get_target_race(self.jra.next_get_time)
        else:
            # より近い方の待機時間に合わせる
            if jra_wait_time > nar_wait_time:
                time_left = nar_wait_time
                self.jra.get_target_race(self.nar.next_get_time)
                self.nar.get_target_race(self.nar.next_get_time)
            else:
                time_left = jra_wait_time
                self.jra.get_target_race(self.jra.next_get_time)
                self.nar.get_target_race(self.jra.next_get_time)

        # どちらも更新されなかった場合(リカバリ処理)
        if time_left == 99999999:
            self.logger.warning('取得処理がどこかおかしいかも')
            self.logger.warning('とりあえず10分待機します')
            time_left = 601

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

    def get_select(self):
        '''取得対象レースを抽出し、オッズ取得を行う'''

        # 中央_暫定オッズ取得処理
        if self.jra_flg:
            self.jra.get_select_realtime()

        # 地方_暫定オッズ取得処理
        if self.nar_flg:
            self.nar.get_select_realtime()

        time.sleep(2)

        # 中央_確定オッズ取得処理
        if self.jra_flg:
            self.jra.get_select_confirm()

        # 地方_確定オッズ取得処理
        if self.nar_flg:
            self.nar.get_select_confirm()

    def record_odds(self):
        '''取得したオッズデータをCSVに書き出す'''

        # 記録データが格納されていてx分40秒を過ぎていなければCSV出力
        if int(jst.second()) <= 40:
            if self.jra_flg:
                if len(self.jra.write_data) != 0:
                    self.jra.record_odds()

            if self.nar_flg:
                if len(self.nar.write_data) != 0:
                    self.nar.record_odds()