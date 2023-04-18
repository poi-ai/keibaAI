import gethtml
import traceback
import re
from base import Base

class RaceList(Base):
    '''JBISのレース一覧ページからレース情報とレースへのリンクを取得する'''

    def __init__(self, race_date, course_id):
        super().__init__()
        self.race_date = race_date
        self.course_id = course_id

    def main(self):
        '''主処理 TODO 後で移植'''

        # HTML取得
        try:
            soup = self.get_soup()
        except Exception as e:
            self.error_output('レース一覧ページのHTML取得処理でエラー', e, traceback.format_exc())
            return False

        # 妥当性/レース情報チェック
        try:
            link_type = self.html_check(soup)
        except Exception as e:
            self.error_output(self.error_reason, e, traceback.format_exc())
            return False

        # レース番号の取得
        try:
            race_no_list = self.get_race_no(soup, link_type)
        except Exception as e:
            self.error_output(self.error_reason, e, traceback.format_exc())
            return False

        return link_type, race_no_list

    def get_soup(self, race_date = None, course_id = None):
        '''
        レース一覧ページからHTML情報を取得する

        Args(任意):
            race_date(str): 取得する対象の日付(yyyyMMddフォーマット)
            course_id(str): 取得する対象のJBIS競馬場ID

        Returns:
            soup(bs4.BeautifulSoup): 取得したレース一覧ページのHTML

        '''
        # 各パラメータが引数で指定されていなければインスタンス変数から持ってくる
        if race_date == None: race_date = self.race_date
        if course_id == None: course_id = self.course_id

        # HTML取得
        return gethtml.soup(f'https://www.jbis.or.jp/race/calendar/{race_date}/{course_id}/')

    def html_check(self, soup):
        '''
        HTMLの妥当性とレース情報をチェックする

        Args:
            soup(bs4.BeautifulSoup): 取得したレース一覧ページのHTML

        Returns:
            link_type(str): レースリンクの種類 (race_table: 出走表、race_result: レース結果)

        '''

        # 中身が空か(取得に失敗)
        if len(soup) == 0:
            self.error_reason = 'HTMLの中身が空です'
            raise

        # パラメータ(日付 or JBIS競馬場ID)が正しくない
        if '指定されたＵＲＬのページは存在しません' in str(soup):
            self.error_reason = '日付かJBIS競馬場IDの値が正しくありません'
            raise

        # パラメータは正しいがその日のレースは存在しない
        if '該当するデータがありません' in str(soup):
            self.error_reason = '指定日/指定競馬場のレースが存在しません'
            raise

        # リンク先は「出走表」か「レース結果」か
        if '２着馬' in str(soup):
            return 'race_result'
        elif '発走時刻' in str(soup):
            return 'race_table'
        else:
            self.error_reason = '未知のフォーマットです'
            raise

    def get_race_no(self, soup, link_type):
        '''
        HTMLの中からレース番号を取得する

        Args:
            soup(bs4.BeautifulSoup): 取得したレース一覧ページのHTML
            link_type(str): レースリンクの種類 (race_table: 出走表、race_result: レース結果)

        Returns:
            list: レース番号リスト

        '''
        if link_type == 'race_table':
            pattern = '/race/{}/{}/(\d+)\.html'.format(self.race_date, self.course_id)
        elif link_type == 'race_result':
            pattern = '/race/result/{}/{}/(\d+)'.format(self.race_date, self.course_id)
        else:
            self.error_reason = 'link_typeの値が正しくありません'
            raise

        return re.findall(pattern, str(soup))