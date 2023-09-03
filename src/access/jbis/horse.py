import gethtml
import mold
import re
import traceback
from base import Base

class Horse(Base):
    def __init__(self):
        super().__init__()

    def set(self, horse_id):
        '''
        Args:
            horse_id(str): 取得対象の競走馬ID
        '''
        self.horse_id = str(horse_id)

    def main(self):
        '''主処理 TODO 後で移行する

        Returns:
            bool: 処理結果

        '''

        # HTML取得
        try:
            soup, result = self.get_soup()
        except Exception as e:
            self.error_output('競走馬ページ取得取得処理でエラー', e, traceback.format_exc())
            return

        if not result: return False

        # 馬名/生産国情報取得
        try:
            self.get_horse_name(soup)
        except Exception as e:
            self.error_output('馬名/生産国情報取得処理でエラー', e, traceback.format_exc())
            return False

        # プロフィール情報取得
        try:
            self.get_profile(soup)
        except Exception as e:
            self.error_output('プロフィール情報取得処理でエラー', e, traceback.format_exc())
            return False

        # 血統情報取得
        try:
            self.get_blood(soup)
        except Exception as e:
            self.error_output('血統情報取得処理でエラー', e, traceback.format_exc())
            return False

        return True

    def get_soup(self, horse_id = None):
        '''
        指定したJBIS競走馬IDの競走馬ページのHTMLをbs4型で取得する

        Args:
            horse_id(int): 取得する対象のJBIS競走馬ID
                ※未指定の場合はインスタンス変数のhorse_idを使用

        Returns:
            soup(bs4.BeautifulSoup): 競走馬ページのHTML
            exist(bool): 指定した競走馬IDが存在するか

        '''
        # 競走馬IDが指定されいない場合はインスタンス変数から引っ張る
        if horse_id == None:
            horse_id = self.horse_id

        # HTML取得
        soup = gethtml.soup(f'https://www.jbis.or.jp/horse/{self.horse_id}/')

        # 存在しないページチェック
        if '指定されたＵＲＬのページは存在しません。' in str(soup):
            return None, False

        return soup, True

    def get_horse_name(self, soup):
        '''
        馬名と生産国を取得する

        Args:
            soup(bs4.BeautifulSoup): 競走馬ページのHTML

        Returns:
            horse_info(dict): 競走馬の情報
                ・horse_name(馬名)
                ・country(生産国)

        '''

        horse_info = {}

        # ページタイトルを取得
        title = soup.find('title').text

        # 馬名を取得
        horse_info['horse_name'] = title[:title.find('｜')]

        # 生産国判定(海外馬は末尾に国の略名が付く)
        m = re.search('(.+)\((.+)\)', horse_info['horse_name'])
        if m != None:
            horse_info['horse_name'] = m.groups()[0]
            horse_info['country'] = m.groups()[1]
        else:
            horse_info['country'] = 'JPN'

        return horse_info

    def get_profile(self, soup):
        '''
        馬の基本情報を取得する

        Args:
            soup(bs4.BeautifulSoup): 競走馬ページのHTML

        Returns:
            horse_info(dict): 競走馬の情報
                ・birthday(誕生日)
                ・hair_color(毛色)
                ・birth_place(生産地)
                ・select_sale_year(セレクトセールが行われた年)
                ・select_sale_price(セレクトセールでの取引額)
                ・select_sale_id(取引されたセレクトセールのJBISID)
                ・select_sale_name(取引されたセレクトセール名)
                ・owner_id(馬主のJBISID)
                ・owner_name(馬主名)
                ・trainer_id(調教師のJBISID)
                ・trainer_name(調教師の所属)
                ・breeder_id(生産牧場のJBISID)
                ・breeder_name(生産牧場名)
            bool: プロフィールテーブルが正確に存在しているか

        '''
        horse_info = {
            'birthday': '',
            'hair_color': '',
            'birth_place': '',
            'select_sale_year': '',
            'select_sale_price': '',
            'select_sale_id': '',
            'select_sale_name': '',
            'owner_id': '',
            'owner_name': '',
            'trainer_id': '',
            'trainer_name': '',
            'breeder_id': '',
            'breeder_name': ''
        }

        # プロフィールテーブルの取得
        profile_table = soup.find_all('table', class_ = 'tbl-data-05 reset-mb-40')

        # 取得失敗時のログ出力
        if len(profile_table) == 0:
            self.logger.error('プロフィールテーブルが見つかりません')
            return None, False
        elif len(profile_table) > 1:
            self.logger.warning('プロフィールテーブルが複数見つかりました。一番上のテーブルを取得対象にします')

        # テーブルの各セルのテキストを全て取得し、リスト化
        profiles = re.findall(r'<.+>(.+?)</.+>', mold.rm_charcode(str(profile_table[0])))

        # 取得失敗時のログ出力
        if len(profiles) == 0:
            self.logger.info('プロフィールテーブルのカラムが見つかりません')
            return None, False

        # リンクのないデータの取得
        for index, profile in enumerate(profiles):
            # 最後の要素の場合は弾く
            if index == len(profiles) - 1 : break

            next_param = profiles[index + 1]

            if profile == '生年月日' and re.search('\d+/\d+/\d+', next_param) != None:
                horse_info['birthday'] = next_param

            if profile == '毛色' and '毛' in next_param:
                horse_info['hair_color'] = next_param.replace('毛', '')

            if profile == '産地' and '産' in next_param:
                horse_info['birth_place'] = next_param.replace('産', '')

            if profile == '市場取引' and index + 3 < len(profiles):
                horse_info['select_sale_year'] = next_param.replace('年', '')
                horse_info['select_sale_price'] = profiles[index + 2].replace('万円', '')

                select_sale_match = re.search('/seri/.+/(.+)/">(.+)</a>', str(profile_table[0]))
                if select_sale_match != None:
                    horse_info['select_sale_id'], horse_info['select_sale_name'] = select_sale_match.groups()
                else:
                    horse_info['select_sale_name'] = profiles[index + 3]

        # リンク付きデータの取得
        # 馬主
        owner_match = re.search('/horse/owner/(.+)/">(.+)</a>', str(profile_table[0]))
        if owner_match != None:
            horse_info['owner_id'], horse_info['owner_name'] = owner_match.groups()

        # 調教師
        trainer_match = re.search('/horse/trainer/(.+)/">(.+)</a>(.+)</td>', str(profile_table[0]))
        if trainer_match != None:
            horse_info['trainer_id'], horse_info['trainer_name'], horse_info['trainer_belong'] = trainer_match.groups()
            horse_info['trainer_belong'] = mold.rm(horse_info['trainer_belong']).replace('（', '').replace('）', '')

        # 生産牧場
        breeder_match = re.search('/breeder/(.+)/">(.+)</a>', str(profile_table[0]))
        if breeder_match != None:
            horse_info['breeder_id'], horse_info['breeder_name'] = breeder_match.groups()

        return horse_info, True

    def get_blood(self, soup):
        '''
        血統表情報を取得する

        Args:
            soup(bs4.BeautifulSoup): 競走馬ページのHTML

        Returns:
            blood_info(dict): 競走馬の血統情報
                ・father_id(父のJBIS競走馬ID)
                ・father_name(父の名前)
                ・mother_id(母のJBIS競走馬ID)
                ・mother_name(母の名前)
                ・ff_id(父父のJBIS競走馬ID)
                ・ff_name(父父の名前)
                ・fm_id(父母のJBIS競走馬ID)
                ・fm_name(父母の名前)
                ・mf_id(母父のJBIS競走馬ID)
                ・mf_name(母父の名前)
                ・mm_id(母母のJBIS競走馬ID)
                ・mm_name(母母の名前)
            bool: 血統表テーブルが正確に存在しているか

        '''
        blood_info = {
            'father_id': '',
            'father_name': '',
            'mother_id': '',
            'mother_name': '',
            'ff_id': '',
            'ff_name': '',
            'fm_id': '',
            'fm_name': '',
            'mf_id': '',
            'mf_name': '',
            'mm_id': '',
            'mm_name': ''
        }

        # 血統表テーブルを取得
        blood_table = soup.find_all('table', class_ = 'tbl-pedigree-01 reset-mb-40')

        # 取得失敗時のログ出力
        if len(blood_table) == 0:
            self.logger.error('血統表テーブルが見つかりません')
            return None, False
        elif len(blood_table) > 1:
            self.logger.warning('血統表テーブルが複数見つかりました。一番上のテーブルを取得対象にします')

        blood = blood_table[0]

        # 両親
        blood_info['father_id'], blood_info['father_name'] = self.blood_match(blood.find('th', class_ = 'male'))
        blood_info['mother_id'], blood_info['mother_name'] = self.blood_match(blood.find('th', class_ = 'female'))

        # 祖父
        ground_father = blood.find_all('td', class_ = 'male')
        blood_info['ff_id'], blood_info['ff_name'] = self.blood_match(ground_father[0])
        blood_info['mf_id'], blood_info['mf_name'] = self.blood_match(ground_father[1])

        # 祖母
        ground_mother = blood.find_all('td', class_ = 'female')
        blood_info['fm_id'], blood_info['fm_name'] = self.blood_match(ground_mother[0])
        blood_info['mm_id'], blood_info['mm_name'] = self.blood_match(ground_mother[1])

        return blood_info, True

    def blood_match(self, frame):
        '''
        血統表テーブルの指定した枠から競走馬IDと競走馬名を抜き出す

        Args:
            frame(str): 血統表の中の1枠分のHTML

        Return:
            tuple(horse_id(str), horse_name(str)): 競走馬名と競走馬ID

        '''
        match = re.search('<a href="/horse/(.*)/">(.*)</a>', str(frame))
        if match != None:
            return match.groups()
        else:
            return ('', '')

if __name__ == '__main__':
    # キタサンブラック
    h = Horse('0001155349')
    # イクイノックス
    #h = Horse('0001309176')
    # オグリ
    #h = Horse('0000177650')
    # ウシュバ
    #h = Horse('0001232861')
    #h = Horse('')
    #h = Horse('')
    #h = Horse('')
    h.main()
