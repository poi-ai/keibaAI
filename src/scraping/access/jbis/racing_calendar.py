import gethtml
import jst
import re
from base import Base

class RacingCalendar(Base):
    '''JBISレーシングカレンダーページから開催情報の取得を行う'''

    def __init__(self, oldest_date, latest_date, association = '1'):
        '''

        Args:
            oldest_date(str) : 取得対象の最古の日付
            latest_date(str) : 取得対象の最新の日付
            association(str) : 取得対象は中央か地方か両方か、1:両方 2:中央のみ 3:地方のみ

        '''
        super().__init__()
        self.oldest_date = oldest_date
        self.latest_date = latest_date
        self.association = association

    def get(self):
        '''JBISレーシングカレンダーページから開催情報の取得を行う

        Return:
            hold_list[[開催日<str>, 競馬場ID<str>],...] : 指定期間内の開催情報のリスト

        '''
        hold_list = []

        # ひと月ずつ開催情報を取得する
        for month in jst.between_month(self.oldest_date, self.latest_date):
            # HTML取得
            soup = self.get_soup(month)

            # レーシングカレンダーテーブル取得
            hold_list = self.get_hold(soup)

            # 開催情報切り出し
            extraction_hold_list = self.extraction_hold(hold_list)

            # 中央のみor地方のみor両方を切り出して返す
            if self.association == '1':
                hold_list += extraction_hold_list
            elif self.association == '2':
                hold_list += self.jra(extraction_hold_list)
            elif self.association == '3':
                hold_list += self.nar(extraction_hold_list)

        return hold_list

    def get_soup(self, month):
        '''指定ページした年月(yyyymm型)のcalendarページのHTMLを取得'''
        return gethtml.soup(f'https://www.jbis.or.jp/race/calendar/{month}/')

    def get_hold(self, soup):
        '''レーシングカレンダーテーブルを取得する

        Args:
            soup(bs4.BeautifulSoup) : 対象ページのHTML

        Returns:
            list[[開催日<str>, 競馬場ID<str>],[開催日<str>, 競馬場ID<str>]...]
        '''

        # レーシングカレンダーテーブルの取得
        calendar_table = soup.find_all('table', class_ = 'tbl-calendar-01')

        # 取得失敗時のログ出力
        if len(calendar_table) == 0:
            self.logger.error('レーシングカレンダーテーブルが見つかりません')
            return
        elif len(calendar_table) > 1:
            self.logger.warning('レーシングカレンダーテーブルが複数見つかりました。一番上のテーブルを取得対象にします')

        table = calendar_table[0]

        # 開催ページのリンクを取得
        link_match = re.findall(r'<a href="/race/calendar/(\d+)/(\d+)/">', str(table))
        if link_match == None:
            self.logger.warning('レーシングカレンダーテーブル内に開催リンクが見つかりません')
            return None

        # タプルをリストにして返す
        return [list(item) for item in link_match]

    def extraction_hold(self, hold_list):
        '''指定した期間内に合致する開催情報を返す

        Args:
            list[[開催日<str>, 競馬場ID<str>],...] : get_hold()で取得した開催情報リスト

        Returns:
            list[[開催日<str>, 競馬場ID<str>],...] : 指定期間内の開催情報リスト
        '''
        return [hold for hold in hold_list if self.oldest_date <= hold[0] <= self.latest_date]

    def nar(self, hold_list):
        '''引数で与えられたJBIS開催情報リストの中から地方の開催情報のみ返す

        Args:
            list[[開催日<str>, 競馬場ID<str>],...] : get_hold()で取得した開催情報リスト

        Returns:
            list[[開催日<str>, 競馬場ID<str>],...] : 引数のリストの中の地方開催情報リスト
        '''
        return [hold for hold in hold_list if 201 <= int(hold[1])]

    def jra(self, hold_list):
        '''引数で与えられたJBIS開催情報リストの中から中央の開催情報のみ返す

        Args:
            list[[開催日<str>, 競馬場ID<str>],...] : get_hold()で取得した開催情報リスト

        Returns:
            list[[開催日<str>, 競馬場ID<str>],...] : 引数のリストの中の中央開催情報リスト
        '''
        return [hold for hold in hold_list if int(hold[1]) <= 110]