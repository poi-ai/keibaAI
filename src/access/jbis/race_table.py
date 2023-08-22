import culc
import gethtml
import mold
import traceback
import re
from base import Base

class RaceTable(Base):
    '''JBISから馬柱を取得する'''
    def __init__(self, race_date, course_id, race_no):
        super().__init__()
        self.race_date = race_date
        self.course_id = course_id
        self.race_no = race_no

    def main(self):
        '''主処理 TODO 後で移植'''

        # HTMLファイルからデータ取得
        soup = self.get_soup()

        # レース概要を取得
        try:
            self.get_race_summary(soup)
        except Exception as e:
            self.error_output('レース概要取得処理でエラー', e, traceback.format_exc())

        # レース結果情報を取得
        try:
            self.get_horse_data(soup)
        except Exception as e:
            self.error_output('出走馬情報取得処理でエラー', e, traceback.format_exc())

    def get_soup(self, race_date = None, course_id = None, race_no = None):
        '''
        指定したJBISレースIDのレース結果ページのHTMLをbs4型で取得する

        Args:

        Returns:
            soup(bs4.BeautifulSoup): レース結果ページのHTML
            exist(int): 指定したレースIDが存在するか
                1: 存在している
                2: 存在しているが、レース結果が出ていない
                3: 存在しない

        '''
        # 各パラメータが引数で指定されていなければインスタンス変数から持ってくる
        if race_date == None: race_date = self.race_date
        if course_id == None: course_id = self.course_id
        if race_no == None: race_no = self.race_no

        # HTML取得
        soup = gethtml.soup(f'https://www.jbis.or.jp/race/{race_date}/{course_id}/{race_no}.html')

        # 結果公開/未公開チェック
        if '該当するデータは存在しません' in str(soup): return 2

        # レースID存在チェック
        if '指定されたＵＲＬのページは存在しません。' in str(soup): return 3

        return soup, 1

    def get_race_summary(self, soup):
        '''
        レース概要を取得

        Args:
            soup(bs4.BeautifulSoup): 出走表ページのHTML

        Reutrns:
            race_info(dict): レース情報
                ・race_name(レース名)
                ・race_class(レースのクラス)
                ・race_type(レース馬場区分[芝/ダート])
                ・distance(距離)
                ・age_term(出走条件[馬齢])
                ・country_term(出走条件[国籍])
                ・local_term(出走条件[地方馬])
                ・load_type(斤量種別)
                ・gender_term(出走条件[性別])
                ・first_prize(1着賞金)
                ・second_prize(2着賞金)
                ・third_prize(3着賞金)
                ・fourth_prize(4着賞金)
                ・fifth_prize(5着賞金)
            bool: 処理結果

        '''
        race_info = {
            'race_name': '',
            'race_class': '',
            'race_type': '',
            'distance': '',
            'age_term': '',
            'country_term': '',
            'local_term': '',
            'load_type': '',
            'gender_term': '',
            'first_prize': '',
            'second_prize': '',
            'third_prize': '',
            'fourth_prize': '',
            'fifth_prize': ''
        }

        # ヘッダのレース番号・レース名を取得
        race_header = soup.find_all('div', class_ = 'box-inner reset-pt-10')
        if len(race_header) == 0:
            self.logger.error('JBIS出走表ページでタイトルの取得に失敗しました')
            return None, False
        elif len(race_header) >= 2:
            self.logger.warning('JBIS出走表ページでタイトルクラスが複数見つかりました。最初のタグから抽出を行います。')

        # TODO 間に空白が入ってるレースで調査
        race_name = re.search(f'(.*)　(.*)', race_header[0].text)
        if race_name == None:
            self.logger.error('JBIS出走表ページでレース名の取得に失敗しました')
        else:
            race_info['race_name'], race_info['race_class'] = race_name.groups()

        # タイトルの横につく画像からTODOを取得
        str_race_header = str(race_header)
        # TODO ここにstr_race_headerの画像から判断できる情報を取得

        # レース概要を取得
        race_summary = soup.find_all('div', class_ = 'box-note-01')
        if len(race_summary) == 0:
            self.logger.error('JBIS出走表ページでレース概要の取得に失敗しました')
            return
        elif len(race_summary) >= 2:
            self.logger.warning('JBIS出走表ページでレース概要クラスが複数見つかりました。最初のタグから抽出を行います。')

        # コース情報
        course_summary = re.search('(.)(\d+)M', str(race_summary[0].find('em')))
        if course_summary == None:
            self.logger.error('JBIS出走表ページでコース情報の取得に失敗しました')
        else:
            race_info['race_type'], race_info['distance'] = course_summary.groups()

        # レース条件
        race_condition_summary = str(race_summary[0].find_all('li', class_ = 'first-child')[0])

        # 馬齢条件
        age_term_match = re.search('サラ系(.)歳(.)', race_condition_summary)

        if age_term_match == None:
            if 'サラ系一般' in race_condition_summary:
                race_info['age_term'] = '一般'
            else:
                self.logger.error('JBIS出走表ページで馬齢条件の取得に失敗しました')
        else:
            if age_term_match.groups()[1] == '上':
                race_info['age_term'] = mold.full_to_half(age_term_match.groups()[0]) + '歳上'
            else:
                race_info['age_term'] = mold.full_to_half(age_term_match.groups()[0]) + '歳'

        # 国籍条件
        if '（国際）' in race_condition_summary:
            race_info['country_term'] = '国際'
        elif '（混合）' in race_condition_summary:
            race_info['country_term'] = '混合'

        # 地方条件
        if '（特指）' in race_condition_summary:
            race_info['local_term'] = '特指'
        elif '（指定）' in race_condition_summary: # TODO カク指、マル指
            race_info['local_term'] = '指定'

        # 斤量条件
        if '定量' in race_condition_summary:
            race_info['load_type'] = '定量'
        elif '馬齢' in race_condition_summary:
            race_info['load_type'] = '馬齢'
        elif '別定' in race_condition_summary:
            race_info['load_type'] = '別定'
        elif 'ハンデ' in race_condition_summary:
            race_info['load_type'] = 'ハンデ'

        # 性別条件
        if '牡・牝' in race_condition_summary:
            race_info['gender_term'] = '牡牝'
        elif '牝' in race_condition_summary:
            race_info['gender_term'] = '牝'

        # クラス名のないliタグ内から情報取得
        for li in race_summary[0].find_all('li'):
            # 1着賞金
            first_prize_match = re.search('1着：(.+)円', str(li))
            if first_prize_match != None:
                race_info['first_prize'] = first_prize_match.groups()[0].replace(',', '')

            # 2着賞金
            second_prize_match = re.search('2着：(.+)円', str(li))
            if second_prize_match != None:
                race_info['second_prize'] = second_prize_match.groups()[0].replace(',', '')

            # 3着賞金
            third_prize_match = re.search('3着：(.+)円', str(li))
            if third_prize_match != None:
                race_info['third_prize'] = third_prize_match.groups()[0].replace(',', '')

            # 4着賞金
            fourth_prize_match = re.search('4着：(.+)円', str(li))
            if fourth_prize_match != None:
                race_info['fourth_prize'] = fourth_prize_match.groups()[0].replace(',', '')

            # 5着賞金
            fifth_prize_match = re.search('5着：(.+)円', str(li))
            if fifth_prize_match != None:
                race_info['fifth_prize'] = fifth_prize_match.groups()[0].replace(',', '')

        return race_info, False

    def get_horse_data(self, soup):
        '''
        出馬表からデータ抽出

        Args:
            soup(bs4.BeautifulSoup): 出走表ページのHTML

        Returns:
            horse_info_list[dict, dict]: 出走馬情報のリスト
                ・horse_no(馬番)
                ・frame_no(枠番)
                ・gender(性別)
                ・age(馬齢)
                ・hair_color(毛色)
                ・horse_id(JBIS競走馬ID)
                ・horse_name(馬名)
                ・trainer_id(調教師のJBISID)
                ・trainer_name(調教師名)
                ・trainer_belong(調教師の所属)
                ・jockey_id(騎手のJBISID)
                ・jockey_name(騎手名)
                ・load(斤量)
                ・owner_id(馬主のJBISID)
                ・owner_name(馬主名)
                ・breeder_id(生産牧場のJBISID)
                ・breeder_name(生産牧場名)
                ・father_id(父のJBIS競走馬ID)
                ・father_name(父の名前)
                ・mother_id(母のJBIS競走馬ID)
                ・mother_name(母の名前)
                ・mf_id(母父のJBIS競走馬ID)
                ・mf_name(母父の名前)
            bool: 処理結果

        '''
        tables = soup.find_all('table', class_ = 'tbl-data-04 tbl-nomination')
        if len(tables) == 0:
            self.logger.error('JBIS出走表ページで出走表テーブルの取得に失敗しました')
            return None, False
        elif len(tables) >= 2:
            self.logger.warning('JBIS出走表ページで出走表テーブルが複数見つかりました。最初に出現したテーブルから抽出を行います。')

        horse_info_list = []

        # 出馬表テーブルから一行ずつ取得
        for index, tr in enumerate(tables[0].find_all('tr')):
            # 一行目はカラム名なのでスキップ
            if index == 0: continue

            horse_info = {
                'horse_no': '',
                'frame_no': '',
                'gender': '',
                'age': '',
                'hair_color': '',
                'horse_id': '',
                'horse_name': '',
                'trainer_id': '',
                'trainer_name': '',
                'trainer_belong': '',
                'jockey_id': '',
                'jockey_name': '',
                'load': '',
                'owner_id': '',
                'owner_name': '',
                'breeder_id': '',
                'breeder_name': '',
                'father_id': '',
                'father_name': '',
                'mother_id': '',
                'mother_name': '',
                'mf_id': '',
                'mf_name': ''
            }

            # 登録頭数
            self.registed_num = len(tables[0].find_all('tr'))

            # 馬番・枠番
            horse_info['horse_no'], horse_info['frame_no'] = index, culc.frame_no_culc(self.registed_num, index)

            # TODO ここらへんのmatch処理を関数化すべきか 読みやすさはしない方が上だと思う
            # tdタグを全て取得して一つずつ中身をチェック
            for td in tr.find_all('td'):
                summary_match = re.search('([牡|牝|セン])([1-2]?[0-9])<br/>(.{1,2})</td>', str(td))
                if summary_match != None:
                    horse_info['gender'], horse_info['age'], horse_info['hair_color'] = summary_match.groups()

                # 馬名
                horse_match = re.search('<a href="/horse/(\d+)/">(.+)</a>', str(td))
                if horse_match != None:
                    horse_info['horse_id'], horse_info['horse_name'] = horse_match.groups()

                # 調教師
                trainer_match = re.search('<a href="/race/trainer/(\d+)/">(.+)</a>（(.+)）', str(td))
                if trainer_match != None:
                    horse_info['trainer_id'], horse_info['trainer_name'], horse_info['trainer_belong'] = trainer_match.groups()

                # 騎手・斤量・減量騎手
                jockey_match = re.search('<a href="/race/jockey/(\d+)/">(.+)</a>', str(td))
                if jockey_match != None:
                    horse_info['jockey_id'], horse_info['jockey_name'] = jockey_match.groups()
                    horse_info['load'] = td.find('span').text
                    # TODO 減量チェック処理

                # 馬主
                owner_match = re.search('<a href="/race/owner/(\d+)/">(.+)</a>', str(td))
                if owner_match != None:
                    horse_info['owner_id'], horse_info['owner_name'] = owner_match.groups()

                # 生産牧場
                breeder_match = re.search('<a href="/breeder/(\d+)/">(.+)</a>', str(td))
                if breeder_match != None:
                    horse_info['breeder_id'], horse_info['breeder_name'] = breeder_match.groups()

            # liタグを全て取得して一つずつ中身をチェック
            for li in tr.find_all('li'):
                # 父名
                father_match = re.search('父：<a href="/horse/(\d+)/"(.+)</a>', str(li))
                if father_match != None:
                    horse_info['father_id'], horse_info['father_name'] = father_match.groups()

                # 母名
                mother_match = re.search('母：<a href="/horse/(\d+)/"(.+)</a>', str(li))
                if mother_match != None:
                    horse_info['mother_id'], horse_info['mother_name'] = mother_match.groups()

                # 母父名
                groundfather_match = re.search('母父：<a href="/horse/(\d+)/"(.+)</a>', str(li))
                if groundfather_match != None:
                    horse_info['mf_id'], horse_info['mf_name'] = groundfather_match.groups()

            horse_info_list.append(horse_info)

        return horse_info_list, True