import config
import jst
import traceback
from execbase import ExecBase
#from jbis.calendar import Calendar

class PastRace(ExecBase):
    def __init__(self):
        super().__init__()
        self.oldest_date = config.OLDEST_DATE
        self.latest_date = config.LATEST_DATE

    def main(self):
        '''主処理'''
        # 開催情報を取得
        self.get_hold()

        # TODO 開催情報からレース情報(レースIDを取得)

    def get_hold(self):
        '''JBISから開催情報を取得する'''

        # 開催情報リスト
        hold_list = []

        # jbisのカレンダー処理を呼びだし
        calendar = self.access.jbis.racing_calendar
        calendar.set(self.oldest_date, self.latest_date)

        # ひと月ずつ開催情報を取得
        for month in jst.between_month(self.oldest_date, self.latest_date):

            # HTML取得
            try:
                soup = calendar.get_soup(month)
            except Exception as e:
                self.error_output('JBISレーシングカレンダーHTML取得処理でエラー', e, traceback.format_exc())
                return

            # レーシングカレンダーテーブル取得
            try:
                month_hold_list = calendar.get_hold(soup)
            except Exception as e:
                self.error_output('JBISレーシングカレンダーテーブル取得処理でエラー', e, traceback.format_exc())
                return

            # 開催情報切り出し
            try:
                extraction_hold_list = calendar.extraction_hold(month_hold_list)
            except Exception as e:
                self.error_output('開催情報切り出し処理でエラー', e, traceback.format_exc())
                return

            hold_list += extraction_hold_list

        print(hold_list)

        return hold_list

if __name__ == '__main__':
    p = PastRace()
    p.set()
    p.main()
