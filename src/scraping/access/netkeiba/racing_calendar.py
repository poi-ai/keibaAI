import gethtml
import itertools
import jst
import re
from base import Base

class Calendar(Base):
    '''netkeibaの中央競馬レーシングカレンダーページから開催日の取得を行う'''

    def __init__(self, oldest_date, latest_date):
        '''
        Args:
            oldest_date(str) : 取得対象の最古の日付(yyyyMMdd) >= 19860101
            latest_date(str) : 取得対象の最新の日付(yyyyMMdd) >= oldest_date

        '''
        super().__init__()
        self.oldest_date = oldest_date
        self.latest_date = latest_date

    def get(self):
        '''netkeibaのレーシングカレンダーページから開催の取得を行う

        Return:
            date_list(list[開催日(yyyyMMdd), 開催日(yyyyMMdd),...]): 指定期間内の開催日のリスト

        '''
        date_list = []

        # ひと月ずつ開催日を取得する
        for year_and_month in jst.between_month(self.oldest_date, self.latest_date):
            year, month = year_and_month[:4], year_and_month[4:]

            # HTML取得
            soup = self.get_soup(year, month)

            # 指定月の開催日をすべて取得
            month_date_list = self.get_date(soup, year, month)

            # 月の開催日から指定期間に含まれない開催日を除去
            extraction_date_list = self.extraction_date(month_date_list)

            date_list.append(extraction_date_list)

        return list(itertools.chain.from_iterable(date_list))

    def get_soup(self, year, month):
        '''指定ページした年月(yyyymm型)のcalendarページのHTMLを取得'''
        return gethtml.soup(f'https://race.netkeiba.com/top/calendar.html?year={year}&month={month}')

    def get_date(self, soup, year, month):
        '''レーシングカレンダーのリンクから開催日を取得する

        Args:
            soup(bs4.BeautifulSoup) : 対象ページのHTML
            year(str): 対象の年
            month(str): 対象の月

        Returns:
            date_list(list[開催日(yyyyMMdd), 開催日(yyyyMMdd),...]): 指定年月の全開催日のリスト
        '''

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

    def extraction_date(self, hold_list):
        '''指定した期間内にのリンクの日付のみ駆り出して返す

        Args:
            list[開催日(yyyyMMdd), 開催日(yyyyMMdd) : 開催日のリスト

        Returns:
            extraciton_list(list[開催日(yyyyMMdd), 開催日(yyyyMMdd)): 指定期間内の開催日のリスト

        '''
        extraciton_list = [hold for hold in hold_list if self.oldest_date <= hold <= self.latest_date]

        return extraciton_list