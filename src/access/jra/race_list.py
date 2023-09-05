import dataframe
import jst
import re
from base import Base
from datetime import datetime
from do_action import DoAction
from bs4 import BeautifulSoup

class RaceList(Base, DoAction):
    def __init__(self):
        super().__init__()

    def get_race_list_page_cname(self, page_type):
        '''
        稼働日の競馬場別レース出走表／オッズ一覧ページのCNAMEパラメータを取得する

        Args:
            page_type(str or int): 取得対象の種別
                1: 出走表一覧ぺージ、2: オッズ一覧ぺージ

        Returns:
            list[str, str,...]: 開催ページのCNAMEパラメータ一覧
                ※対象レースがない場合は空配列を返す
        '''
        if str(page_type) != '1' and str(page_type) != '2':
            raise

        # 今週の開催一覧ページのHTMLを取得
        if str(page_type) == '1':
            soup = self.do_action(self.RACE_BASE_URL, 'pw01dli00/F3')
        else:
            soup = self.do_action(self.ODDS_BASE_URL, 'pw15oli00/6D')

        # 日付ごとの枠 > 枠内に開催別ページへのリンクがあるため、
        # まずは枠ごとにリスト化し、各枠の日付を切り出す
        hold_frame = soup.find('div', id = 'main')
        soup = BeautifulSoup(str(hold_frame), 'lxml')
        hold_dates = soup.find_all('h3')

        for i, hold_date in enumerate(hold_dates):
            # レース日と稼働日が一致する枠の番号を取得
            m = re.search(r'(\d+)月(\d+)日', str(hold_date))
            '''TODO 動作確認後に削除
            ・レース開催日 if jst.month() == m.group(1) and jst.day() == m.group(2):
            ・月～水曜日 if '直近レース開催の月' == m.group(1) and '直近レース開催の日' == m.group(2):
            ・木～金曜日 動作確認不可(JRAの今週の開催ページに出走表へのリンクがないため)
            '''
            if jst.month() == m.group(1) and '3' == m.group(2):
                # 合致した枠内のHTMLを取得
                links = BeautifulSoup(str(soup.find_all('div', class_ = 'link_list multi div3 center')[i]), 'lxml')
                return self.extract_param(links)

        return []

    def get_race_info(self, cname):
        '''
        開催一覧ページからレース概要情報を取得する

        Args:
            cname(str): 対象ページのCNAMEパラメータ
                get_race_list_page_cname()から取得可

        Returns:
            race_info(pandas.DataFrame): レース概要情報
                発走時刻・レース名・変更・コース距離・頭数
                TODO 競馬場名も入れたい
        '''
        soup = self.do_action(self.RACE_BASE_URL, cname)
        info_table = dataframe.get_table(str(soup))[0]

        # 存在しているはずのカラムが取れていなかったらエラーとみなす
        if not '発走時刻' in info_table.columns:
            raise

        course = []
        horse_num = []
        # データ成形
        for i in info_table.index:
            # 発走時刻をdatetime型に
            m = re.search(r'(\d+)時(\d+)分', info_table['発走時刻'][i])
            info_table['発走時刻'][i] = datetime(int(jst.year()), int(jst.month()), int(jst.day()), int(m.group(1)), int(m.group(2)), 0)

            m = re.search(r'(.+)m(.+)', info_table['コース距離頭数'][i])
            course.append(m.group(1))
            horse_num.append(m.group(2))

        # 作成したカラムを追加
        info_table['コース距離'] = course
        info_table['頭数'] = horse_num

        # いらない(使えない)カラムは消す
        if 'レース番号' in info_table.columns: info_table = info_table.drop(columns = ['レース番号'])
        if '馬体重' in info_table.columns: info_table = info_table.drop(columns = ['馬体重'])
        if '出馬表' in info_table.columns: info_table = info_table.drop(columns = ['出馬表'])
        if 'オッズ' in info_table.columns: info_table = info_table.drop(columns = ['オッズ'])
        if 'レース結果' in info_table.columns: info_table = info_table.drop(columns = ['レース結果'])
        if 'レース映像' in info_table.columns: info_table = info_table.drop(columns = ['レース映像'])
        if 'WIN5' in info_table.columns: info_table = info_table.drop(columns = ['WIN5'])
        if 'コース距離頭数' in info_table.columns: info_table = info_table.drop(columns = ['コース距離頭数'])

        return info_table

    def get_odds_page_cname(self, cname):
        '''
        開催一覧ページからオッズページのCNAMEパラメータを取得する

        Args:
            cname(str): 対象ページのCNAMEパラメータ
                get_race_list_page_cname()から取得可

        Retuns:
            odds_page_cname_list(list[str, str,..]): 取得したオッズページのCNAMEリスト
        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

        # TODO ↓ここやり直し
        # キーを持っていないので、抜けがある券種(少頭数レースの枠連とか)があるとずれる
        # レース単位でチェックする処理に変える

        # 各券種別のオッズページのパラメータを取得
        odds_param_dict = {
            'tanpuku': [self.extract_param(str(i))[0] for i in soup.find_all('div', class_ = 'tanpuku')],
            'wakuren': [self.extract_param(str(i))[0] for i in soup.find_all('div', class_ = 'wakuren')],
            'umaren': [self.extract_param(str(i))[0] for i in soup.find_all('div', class_ = 'umaren')],
            'wide': [self.extract_param(str(i))[0] for i in soup.find_all('div', class_ = 'wide')],
            'umatan': [self.extract_param(str(i))[0] for i in soup.find_all('div', class_ = 'umatan')],
            'trio': [self.extract_param(str(i))[0] for i in soup.find_all('div', class_ = 'trio')],
            'tierce': [self.extract_param(str(i))[0] for i in soup.find_all('div', class_ = 'tierce')]
        }

        return odds_param_dict

# TODO サンプルコード 後で消す
import mold
rl = RaceList()
print(mold.tidy_dict(rl.get_odds_page_cname(rl.get_race_list_page_cname('2'))))