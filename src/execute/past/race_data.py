import itertools
import jst
import traceback
from execbase import ExecBase

class RaceData(ExecBase):
    # TODO initに引数持たせられないかもしれない問題
    def __init__(self, oldest_date, latest_date, association = 0):
        '''
        過去のレースデータを取得する

        Args:
            oldest_date(int or str): 取得対象の最も古い日付
                中央 >= 20070728, 地方 >= 20150225
            latest_date(int or str): 取得対象の最も新しい日付
            association(int): 取得対象
                -1: 中央、0: 両方、1: 地方

        Returns:
            TODO

        '''
        super().__init__()
        self.oldest_date = str(oldest_date)
        self.latest_date = str(latest_date)
        # TODO 日付妥当性チェック処理とか入れたい
        self.association = association

    def main(self):
        '''主処理'''

        jra_date_list = []
        nar_date_list = []

        # 中央競馬の開催日を取得
        if self.association <= 0:
            racing_calender = self.access.netkeiba.jra.racing_calendar
            date_list = []

            # 月ごとに開催日を取得する
            for year_and_month in jst.between_month(self.oldest_date, self.latest_date):
                year, month = year_and_month[:4], year_and_month[4:]

                # 指定月の開催日をすべて取得
                try:
                    self.logger.info(f'中央競馬レースカレンダーの開催日取得開始 {year}年{month}月')
                    month_date_list = racing_calender.get_date(year, month)
                    self.logger.info(f'中央競馬レースカレンダーの開催日取得終了 {year}年{month}月')
                except Exception as e:
                    self.error_output(f'中央競馬レースカレンダーの開催日取得に失敗しました {year}年{month}月', e, traceback.format_exc())
                    continue

                # 月の中で指定した期間内に収まる開催日のみ切り出し
                month_date_list = [date for date in month_date_list if self.oldest_date <= date <= self.latest_date]

                date_list.append(month_date_list)

            # 二重配列になっているので一元化
            jra_date_list = list(itertools.chain.from_iterable(date_list))

        # 地方競馬の開催日(=毎日)を取得
        if self.association >= 0:
            nar_date_list = jst.between_date(self.oldest_date, self.latest_date)

        # 取得する開催日が存在していていたら取得用のインスタンスを準備
        if len(jra_race_list) != 0:
            jra_race_list = self.access.netkeiba.jra.race_list
            jra_race_table = self.access.netkeiba.jra.race_table
            #jra_race_result = self.access.netkeiba.jra.race_result

        if len(nar_race_list) != 0:
            nar_race_list = self.access.netkeiba.nar.race_list
            nar_race_table = self.access.netkeiba.nar.race_table
            #nar_race_result = self.access.netkeiba.jra.race_result

        # 一日ごとに情報取得→データ保存を行う
        for date in jst.between_date(self.oldest_date, self.latest_date):

            # 中央のレースデータ取得
            if date in jra_date_list:
                race_id_list = []
                try:
                    self.logger.info(f'中央競馬レースIDの取得開始 対象日: {date[:4]}年{date[4:6]}月{date[6:]}日')
                    race_id_list = jra_race_list.get_race_id_list(date)
                    self.logger.info(f'中央競馬レースIDの取得終了 対象日: {date[:4]}年{date[4:6]}月{date[6:]}日')
                except Exception as e:
                    self.error_output('中央競馬レースIDの取得処理でエラー', e, traceback.format_exc())

                if len(race_id_list) != 0:
                    # レースごとにデータの取得・保存
                    for race_id in race_id_list:
                        # 出走表からレース情報取得
                        try:
                            self.logger.info(f'netkeiba出走表からのレース情報取得処理開始 レースID: {race_id}')
                            race_info = jra_race_table.get_race_info(race_id)
                            self.logger.info(f'netkeiba出走表からのレース情報取得処理終了 レースID: {race_id}')
                        except Exception as e:
                            self.error_output('netkeiba出走表からのレース情報取得処理でエラー', e, traceback.format_exc())
                            # TODO 飛ばす処理

                        # TODO CSVに保存
                        pass

                        # TODO DBに保存
                        pass

                        try:
                            self.logger.info(f'netkeibaの出走表からの出走馬情報取得処理開始 レースID: {race_id}')
                            horse_info = jra_race_table.get_horse_info(race_id)
                            self.logger.info(f'netkeibaの出走表からの出走馬情報取得処理終了 レースID: {race_id}')
                        except Exception as e:
                            self.error_output('netkeibaの出走表からの出走馬情報取得処理でエラー', e, traceback.format_exc())
                            # TODO 飛ばす処理

                        # TODO CSVに保存
                        pass

                        # TODO DBに保存
                        pass

                        # TODO レース結果からデータ取得
                        pass

                        # TODO CSVに保存
                        pass

                        # TODO DBに保存
                        pass

            # 地方のレースデータ取得
            if date in nar_date_list:
                race_id_list = []
                try:
                    self.logger.info(f'地方競馬レースIDの取得開始 対象日: {date[:4]}年{date[4:6]}月{date[6:]}日')
                    race_id_list = nar_race_list.get_race_id_list(date)
                    self.logger.info(f'地方競馬レースIDの取得終了 対象日: {date[:4]}年{date[4:6]}月{date[6:]}日')
                except Exception as e:
                    self.error_output('地方競馬レースIDの取得処理でエラー', e, traceback.format_exc())

                if len(race_id_list) != 0:
                    # レースごとにデータの取得・保存
                    for race_id in race_id_list:
                        # TODO 出走表からデータ取得
                        pass

                        # TODO CSVに保存
                        pass

                        # TODO DBに保存
                        pass

                        # TODO レース結果からデータ取得
                        pass

                        # TODO CSVに保存
                        pass

                        # TODO DBに保存
                        pass

        return


# TODO テスト用なので後で消す
r = RaceData(20221215,20230115,-1)
r.main()