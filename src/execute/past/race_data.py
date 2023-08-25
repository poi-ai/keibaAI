from execbase import ExecBase

class RaceData(ExecBase):
    def __init__(self, oldest_date, latest_date, association = 0):
        '''
            過去のレースデータを取得する

            Args:
                oldest_date(str): 取得対象の最も古い日付
                    中央 >= 20070728, 地方 >= 20150225
                latest_date(str): 取得対象の最も新しい日付
                association(int): 取得対象
                    -1: 中央、0: 両方、1: 地方

        '''
        super().__init__()
        self.oldest_date = oldest_date
        self.latest_date = latest_date
        self.association = association

    def main(self):
        '''主処理'''

        # JRAの場合は開催日をレーシングカレンダーから取得
        racing_calender = self.access.netkeiba.racing_calendar()
        race_list = self.access.netkeiba.race_list()
        race_table = self.access.netkeiba.jra()

r = RaceData(20230805,20230807,-1)