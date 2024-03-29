import gethtml
import mold
import traceback
import re
from base import Base

class RaceResult(Base):
    '''JBISのサイトからレース結果を取得する'''

    def __init__(self):
        super().__init__()

    def set(self, race_date, course_id, race_no):
        self.race_date = race_date
        self.course_id = course_id
        self.race_no = race_no

    def main(self):
        '''主処理 TODO 後で消す'''

        # HTMLファイルからデータ取得
        soup, exist = self.get_soup()

        # レース概要を取得
        try:
            self.get_race_summary(soup)
        except Exception as e:
            self.error_output('レース概要取得処理でエラー', e, traceback.format_exc())

        # レース結果情報を取得
        try:
            self.get_horse_result(soup)
        except Exception as e:
            self.error_output('出走馬結果取得処理でエラー', e, traceback.format_exc())

        # ラップタイムを取得
        try:
            self.get_lap(soup)
        except Exception as e:
            self.error_output('ラップタイム取得処理でエラー', e, traceback.format_exc())

        # コーナー通過順位を取得
        try:
            self.get_corner_rank(soup)
        except Exception as e:
            self.error_output('コーナー通過順位取得処理でエラー', e, traceback.format_exc())

    def get_soup(self, race_date = None, course_id = None, race_no = None):
        '''
        指定したJBISレースIDのレース結果ページのHTMLをbs4型で取得する

        Args:
            race_date(str): 対象レースのレース日
            course_id(str): 対象レースのJBIS競馬場ID
            race_no(str): 対象レースのレース番号

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
        soup = gethtml.soup(f'https://www.jbis.or.jp/race/result/{race_date}/{course_id}/{race_no}/')

        # 結果公開/未公開チェック
        if '該当するデータは存在しません' in str(soup): return 2

        # レースID存在チェック
        if '指定されたＵＲＬのページは存在しません。' in str(soup): return 3

        return soup, 1

    def get_race_summary(self, soup):
        '''
        レース概要を取得

        Args:
            soup(bs4.BeautifulSoup): レース結果ページのHTML

        Returns:
            race_result_info(dict): レース情報
                ・race_name(レース名)
                ・race_class(レースのクラス)
                ・race_type(レース馬場区分[芝/ダート])
                ・distance(距離)
                ・age_term(出走条件[馬齢])
                ・country_term(出走条件[国籍])
                ・local_term(出走条件[地方馬])
                ・load_type(斤量種別)
                ・gender_term(出走条件[性別])
                ・weather(天候)
                ・grass_condition(芝の馬場状態)
                ・dirt_condition(ダートの馬場状態)
                ・first_prize(1着賞金)
                ・second_prize(2着賞金)
                ・third_prize(3着賞金)
                ・fourth_prize(4着賞金)
                ・fifth_prize(5着賞金)
            bool: 処理結果

        '''
        race_result_info = {
            'race_name': '',
            'race_class': '',
            'race_type': '',
            'distance': '',
            'age_term': '',
            'country_term': '',
            'local_term': '',
            'load_type': '',
            'gender_term': '',
            'weather': '',
            'grass_condition': '',
            'dirt_condition': '',
            'first_prize': '',
            'second_prize': '',
            'third_prize': '',
            'fourth_prize': '',
            'fifth_prize': ''
        }

        # ヘッダのレース番号・レース名を取得
        race_header = soup.find_all('div', class_ = 'hdg-l2-06-container')
        if len(race_header) == 0:
            self.logger.error('JBISレース結果ページでタイトルの取得に失敗しました')
            return None, False
        elif len(race_header) >= 2:
            self.logger.warning('JBISレース結果ページでタイトルクラスが複数見つかりました。最初のタグから抽出を行います。')

        # TODO 間に空白が入ってるレースで調査
        race_name = re.search(f'{int(self.race_no)}R (.+)　(.+)', race_header[0].text)
        if race_name == None:

            race_name = re.search(f'{int(self.race_no)}R (.+)', race_header[0].text)
            if race_name == None:
                self.logger.error('JBISレース結果ページでレース名の取得に失敗しました')
                self.logger.info(str(race_header[0]))
            else:
                race_result_info['race_name'] = race_name.groups()[0].strip()
                self.logger.info('-------------------------------')
                self.logger.info('レース名は取れた。クラスは取れない')
                self.logger.info(race_header.find_all('img')[0])
                self.logger.info('-------------------------------')
        else:
            race_result_info['race_name'] = race_name.groups()[0].strip()
            race_result_info['race_class'] = race_name.groups()[1].strip()

        # タイトルの横につく画像からTODOを取得
        str_race_header = str(race_header)
        # TODO ここにstr_race_headerの画像から判断できる情報を取得

        # レース概要を取得
        race_summary = soup.find_all('div', class_ = 'box-note-01')
        if len(race_summary) == 0:
            self.logger.error('JBISレース結果ページでレース概要の取得に失敗しました')
            return
        elif len(race_summary) >= 2:
            self.logger.warning('JBISレース結果ページでレース概要クラスが複数見つかりました。最初のタグから抽出を行います。')

        # コース情報
        course_summary = re.search('(.)(\d+)M', str(race_summary[0].find('em')))
        if course_summary == None:
            self.logger.error('JBISレース結果ページでコース情報の取得に失敗しました')
        else:
            race_result_info['race_type'], race_result_info['distance'] = course_summary.groups()

        # レース条件
        race_condition_summary = str(race_summary[0].find_all('li', class_ = 'first-child')[0])

        # 馬齢条件 TODO ない場合が多い、要調査
        age_term_match = re.search('サラ系(.)歳(.)', race_condition_summary)
        if age_term_match == None:
            pass
            #self.logger.error(f'JBISレース結果ページで馬齢条件の取得に失敗しました https://www.jbis.or.jp/race/result/{self.race_date}/{self.course_id}/{self.race_no}/')
        else:
            if age_term_match.groups()[1] == '上':
                race_result_info['age_term'] = mold.full_to_half(age_term_match.groups()[0]) + '歳上'
            else:
                race_result_info['age_term'] = mold.full_to_half(age_term_match.groups()[0]) + '歳'

        # 国籍条件
        if '（国際）' in race_condition_summary:
            race_result_info['country_term'] = '国際'
        elif '（混合）' in race_condition_summary:
            race_result_info['country_term'] = '混合'

        # 地方条件
        if '（特指）' in race_condition_summary:
            race_result_info['local_term'] = '特指'
        elif '（指定）' in race_condition_summary: # TODO カク指、マル指
            race_result_info['local_term'] = '指定'

        # 斤量種別
        if '定量' in race_condition_summary:
            race_result_info['load_type'] = '定量'
        elif '馬齢' in race_condition_summary:
            race_result_info['load_type'] = '馬齢'
        elif '別定' in race_condition_summary:
            race_result_info['load_type'] = '別定'
        elif 'ハンデ' in race_condition_summary:
            race_result_info['load_type'] = 'ハンデ'

        # 性別条件
        if '牡・牝' in race_condition_summary:
            race_result_info['gender_term'] = '牡牝'
        elif '牝' in race_condition_summary:
            race_result_info['gender_term'] = '牝'

        # クラス名のないliタグ内から情報取得
        for li in race_summary[0].find_all('li'):
            # 天候
            weather_match = re.search('天候：(.+)</li>', str(li))
            if weather_match != None:
                race_result_info['weather'] = mold.rm(weather_match.groups()[0])

            # 馬場状態(芝)
            grass_condition_match = re.search('芝：(.+)</li>', str(li))
            if grass_condition_match != None:
                race_result_info['grass_condition'] = mold.rm(grass_condition_match.groups()[0])

            # 馬場状態(ダ) TODO match条件確認(ダかダートか)
            dirt_condition_match = re.search('ダート：(.+)</li>', str(li))
            if dirt_condition_match != None:
                race_result_info['dirt_condition'] = mold.rm(dirt_condition_match.groups()[0])

            # 1着賞金
            first_prize_match = re.search('1着：(.+)円', str(li))
            if first_prize_match != None:
                race_result_info['first_prize'] = first_prize_match.groups()[0].replace(',', '')

            # 2着賞金
            second_prize_match = re.search('2着：(.+)円', str(li))
            if second_prize_match != None:
                race_result_info['second_prize'] = second_prize_match.groups()[0].replace(',', '')

            # 3着賞金
            third_prize_match = re.search('3着：(.+)円', str(li))
            if third_prize_match != None:
                race_result_info['third_prize'] = third_prize_match.groups()[0].replace(',', '')

            # 4着賞金
            fourth_prize_match = re.search('4着：(.+)円', str(li))
            if fourth_prize_match != None:
                race_result_info['fourth_prize'] = fourth_prize_match.groups()[0].replace(',', '')

            # 5着賞金
            fifth_prize_match = re.search('5着：(.+)円', str(li))
            if fifth_prize_match != None:
                race_result_info['fifth_prize'] = fifth_prize_match.groups()[0].replace(',', '')

        return race_result_info, True

    def get_horse_result(self, soup):
        '''
        レース結果情報を取得

        Args:
            soup(bs4.BeautifulSoup): レース結果ページのHTML

        Returns:
            race_result_info_list(list[dict{},...]): 馬別のレース結果情報
                ・rank(着順)
                ・frame_no(枠番)
                ・horse_no(馬番)
                ・horse_id(JBIS競走馬ID)
                ・horse_name(馬名)
                ・father_id(父のJBIS競走馬ID)
                ・father_name(父の名前)
                ・mother_id(母のJBIS競走馬ID)
                ・mother_name(母の名前)
                ・select_sale_year(セレクトセールが行われた年)
                ・select_sale_id(取引されたセレクトセールのJBISID)
                ・select_sale_name(取引されたセレクトセール名)
                ・select_sale_price(セレクトセールでの取引額)
                ・gender(性別)
                ・age(馬齢)
                ・jockey_id(騎手JBISID)
                ・jockey_name(騎手名)
                ・load(斤量)
                ・goal_time(走破タイム)
                ・diff(着差)
                ・pass_rank(コーナー通過順位)
                ・agari(上がり3F)
                ・sp_shisu(スピード指数)
                ・popular(単勝人気)
                ・weight(馬体重)
                ・weight_change(馬体重増減)
                ・trainer_id(調教師のJBISID)
                ・trainer_name(調教師名)
                ・trainer_belong(調教師の所属)
                ・owner_id(馬主のJBISID)
                ・owner_name(馬主名)
                ・breeder_id(生産牧場のJBISID)
                ・breeder_name(生産牧場名)
            bool: 処理結果

        '''
        race_result_info_list = []

        # レース結果テーブルからデータ取得
        # リンクから各種IDをとるためpd.read_htmlは使わない
        result_tables = soup.find_all('table', class_ = 'tbl-data-04 cell-align-c')
        if len(result_tables) == 0:
            self.logger.error('JBISレース結果ページで結果テーブルの取得に失敗しました')
            return None, False
        elif len(result_tables) >= 2:
            self.logger.warning('JBISレース結果ページで結果テーブルが複数見つかりました。最初のタグから抽出を行います。')

        # 各行(=各馬)ごとにデータを取得する
        for row_index, tr in enumerate(result_tables[0].find_all('tr')):
            race_result_info = {
                'rank': '',
                'frame_no': '',
                'horse_no': '',
                'horse_id': '',
                'horse_name': '',
                'father_id': '',
                'father_name': '',
                'mother_id': '',
                'mother_name': '',
                'select_sale_year': '',
                'select_sale_id': '',
                'select_sale_name': '',
                'select_sale_price': '',
                'gender': '',
                'age': '',
                'jockey_id': '',
                'jockey_name': '',
                'load': '',
                'goal_time': '',
                'diff': '',
                'pass_rank': '',
                'agari': '',
                'sp_shisu': '',
                'popular': '',
                'weight': '',
                'weight_change': '',
                'trainer_id': '',
                'trainer_name': '',
                'trainer_belong': '',
                'owner_id': '',
                'owner_name': '',
                'breeder_id': '',
                'breeder_name': ''
            }

            # 最初の行はカラム名なので飛ばす
            if row_index == 0: continue

            # 着順取得
            race_result_info['rank'] = mold.rm(tr.find('th').text)

            # 列を行ごとに区切って対応するデータを取得
            td = tr.find_all('td')

            # 枠番、馬番取得
            race_result_info['frame_no'] = mold.rm(td[0].text)
            race_result_info['horse_no'] = mold.rm(td[1].text)

            # 競走馬ID、競走馬名取得 TODO 出身国、ブリンカー、地方マーク取得
            horse_id_match = re.search('<a href="/horse/(.+)/"><em>(.+)</em>', str(td[2]))
            if horse_id_match is None:
                self.logger.error('JBISレース結果ページで競走馬IDの取得に失敗しました')
            else:
                race_result_info['horse_id'], race_result_info['horse_name'] = horse_id_match.groups()

            # 父名・母名・セレクトセール情報取得
            for li in td[2].find_all('li'):
                # 父名
                father_match = re.search('父：<a href="/horse/(.+)/">(.+)</a>', str(li))
                if father_match != None:
                    race_result_info['father_id'], race_result_info['father_name'] = father_match.groups()

                # 母名
                mother_match = re.search('母：<a href="/horse/(.+)/">(.+)</a>', str(li))
                if mother_match != None:
                    race_result_info['mother_id'], race_result_info['mother_name'] = mother_match.groups()

                # セレクトセール情報
                select_sale_match = re.search('<a href="/seri/(.+)/(.+)/">(.+)</a>', str(li))
                if select_sale_match != None:
                    race_result_info['select_sale_year'], race_result_info['select_sale_id'], race_result_info['select_sale_name'] = select_sale_match.groups()

                select_sale_price_match = re.search('(\d+)\.(\d+)万円', str(li))
                if select_sale_price_match != None:
                    race_result_info['select_sale_price'] = str(int(select_sale_price_match.groups()[0]) * 10000 + int(select_sale_price_match.groups()[1]) * 1000)

            # 性別・馬齢
            try:
                race_result_info['gender'] = td[3].text[:1]
            except:
                self.logger.error(f'https://www.jbis.or.jp/race/result/{self.race_date}/{self.course_id}/{self.race_no}/ horse_no:{race_result_info["horse_no"]}')
                self.logger.error(str(td))
            race_result_info['age'] = td[3].text[1:]

            # 騎手ID・騎手名・斤量 TODO 減量マーク取得
            jockey_match = re.search('"/race/jockey/(.+)/">(.+)</a><br/>(\d\d\.\d)</td>', str(td[4]))
            if jockey_match != None:
                race_result_info['jockey_id'], race_result_info['jockey_name'], race_result_info['load'] = jockey_match.groups()

            # 走破タイム・着差・通過順位・上がり3F・スピード指数・人気
            race_result_info['goal_time'] = mold.change_seconds(td[5].text)
            race_result_info['diff'] = td[6].text
            race_result_info['pass_rank'] = td[7].text
            race_result_info['agari'] = td[8].text
            race_result_info['sp_shisu'] = td[9].text
            race_result_info['popular'] = td[10].text

            # 馬体重・馬体重増減
            weight_match = re.search('<td>(.+)<br/>（(.+)）</td>', str(td[11]))
            if weight_match != None:
                race_result_info['weight'], race_result_info['weight_change'] = weight_match.groups()

            # 調教師ID・調教師名・調教師所属
            trainer_match = re.search('<a href="/race/trainer/(.+)/">(.+)</a><br/>（(.+)）', str(td[12]))
            if trainer_match != None:
                race_result_info['trainer_id'], race_result_info['trainer_name'], race_result_info['trainer_belong'] = trainer_match.groups()

            # 馬主ID・馬主名
            owner_match = re.search('<a href="/race/owner/(.+)/">(.+)</a><br/>', str(td[13]))
            if owner_match != None:
                race_result_info['owner_id'], race_result_info['owner_name'] = owner_match.groups()

            # 生産牧場ID・生産牧場名
            breeder_match = re.search('<a href="/breeder/(.+)/">(.+)</a>', str(td[13]))
            if breeder_match != None:
                race_result_info['breeder_id'], race_result_info['breeder_name'] = breeder_match.groups()

            race_result_info_list.append(race_result_info)

        return race_result_info_list, True

    def get_lap(self, soup):
        '''
        ラップタイムを取得する

        Args:
            soup(bs4.BeautifulSoup): レース結果ページのHTML

        Returns:
            lap_info_list(dict) or None: レースのラップ情報
                ・agari_4f(先頭馬上がり3F)
                ・agari_3f(先頭馬)
                ・lap_time(先頭馬ラップタイム)

        '''
        lap_info = {
            'agari_4f': '',
            'agari_3f': '',
            'lap_time': ''
        }

        # ラップタイムテーブルの存在チェック
        if '<h3 class="hdg-l3-01"><span>タイム</span></h3>' not in str(soup):
            self.logger.info('ラップタイムテーブルが存在しません')
            return None

        # テーブル一覧を取得
        tables = soup.find_all('table', class_ = 'tbl-data-05')

        # ラップタイムテーブルは一番上にある
        lap_time_table = tables[0]

        # 一行ずつチェック
        for tr in lap_time_table.find_all('tr'):

            if tr.find('th').text == '上がり':
                lap_info['agari_4f'], lap_info['agari_3f'] = mold.rm_nl(tr.find('td').text).split('-')

            if tr.find('th').text == 'ハロンタイム':
                lap_info['lap_time'] = tr.find('td').text

        return lap_info

    def get_corner_rank(self, soup):
        '''
        コーナー通過順位を取得する

        Args:
            soup(bs4.BeautifulSoup): レース結果ページのHTML

        Returns:
            corner_rank(dict) or None: 各コーナーの通過順位
                ・corner1_rank(第1コーナーの通過順位)
                ・corner2_rank(第2コーナーの通過順位)
                ・corner3_rank(第3コーナーの通過順位)
                ・corner4_rank(第4コーナーの通過順位)

        '''
        corner_rank = {
            'corner1_rank': '',
            'corner2_rank': '',
            'corner3_rank': '',
            'corner4_rank': '',
        }

        # ラップタイムテーブルの存在チェック
        if '<h3 class="hdg-l3-01"><span>コーナー通過順位</span></h3>' not in str(soup):
            self.logger.info('コーナー通過順位テーブルが存在しません')
            return None

        # テーブル一覧を取得
        tables = soup.find_all('table', class_ = 'tbl-data-05')

        # ラップタイムテーブルがなければ一番上、あれば二番目から取得
        if '<h3 class="hdg-l3-01"><span>タイム</span></h3>' in str(soup):
            corner_rank_table = tables[1]
        else:
            corner_rank_table = tables[0]

        # 一行ずつチェック
        for tr in corner_rank_table.find_all('tr'):
            if tr.find('th').text == '1コーナー':
                corner_rank['corner1_rank'] = mold.rm_nl(tr.find('td').text).replace(',', '|')

            if tr.find('th').text == '2コーナー':
                corner_rank['corner2_rank'] = mold.rm_nl(tr.find('td').text).replace(',', '|')

            if tr.find('th').text == '3コーナー':
                corner_rank['corner3_rank'] = mold.rm_nl(tr.find('td').text).replace(',', '|')

            if tr.find('th').text == '4コーナー':
                corner_rank['corner4_rank'] = mold.rm_nl(tr.find('td').text).replace(',', '|')

        return corner_rank
