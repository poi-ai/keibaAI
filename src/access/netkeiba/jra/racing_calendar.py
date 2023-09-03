import gethtml
import jst
import re
import traceback
from base import Base

class RacingCalendar(Base):
    '''netkeibaの中央競馬レーシングカレンダーページから開催日の取得を行う'''

    def __init__(self):
        super().__init__()

    def get_date(self, year, month):
        '''
        レーシングカレンダーから開催日を取得する

        Args:
            year(str): 取得対象の年
            month(str): 取得対象の月

        Returns:
            date_list(list[str(yyyyMMdd), str(yyyyMMdd),...]): 指定年月の全開催日のリスト
        '''

        # HTMLを取得
        soup = gethtml.soup(f'https://race.netkeiba.com/top/calendar.html?year={year}&month={month}')

        # aタグを取得
        links = soup.find_all('a')
        date_list = []

        for link in links:
            date_url = link.get('href')
            # カレンダー内にあるリンクから開催日を取得
            # 2007年以前と2008年以降でリンク先が異なるので取得ロジックを変える
            if int(year) <= 2007:
                rematch = re.search('race/sum/\d+/(\d+)', str(link))
                if rematch != None:
                    date_list.append(rematch.groups()[0])
                    # 重複削除/ソート
                    date_list = list(set(date_list))
                    date_list.sort()
            elif int(year) > 2007:
                if 'kaisai_date' in date_url:
                    date_list.append(date_url[len(date_url) - 8:])

        return date_list
