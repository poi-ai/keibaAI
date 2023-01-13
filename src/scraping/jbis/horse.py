import base
import gethtml
import mold
import re
import traceback

class Horse(base.Base):
    def __init__(self, horse_id):
        self.horse_id = horse_id

    def main(self):
        '''主処理'''

        # HTML取得
        try:
            soup = gethtml.soup(f'https://www.jbis.or.jp/horse/{self.horse_id}/')
        except Exception as e:
            self.error_output('競走馬ページ取得取得処理でエラー', e, traceback.format_exc())
            return

        # TODO 存在しないページチェック

        # 馬名/生産国情報取得
        try:
            self.get_horse_name(soup)
        except Exception as e:
            self.error_output('馬名/生産国情報取得処理でエラー', e, traceback.format_exc())
            return

        # プロフィール情報取得
        try:
            self.get_profile(soup)
        except Exception as e:
            self.error_output('プロフィール情報取得処理でエラー', e, traceback.format_exc())
            return

        # 血統情報取得
        try:
            self.get_blood(soup)
        except Exception as e:
            self.error_output('血統情報取得処理でエラー', e, traceback.format_exc())
            return

    def get_horse_name(self, soup):
        '''馬名と生産国を取得する'''

        # ページタイトルを取得
        title = soup.find('title').text

        # 馬名を取得
        horse_name = title[:title.find('｜')]

        # 生産国判定(海外馬は末尾に国の略名が付く)
        m = re.search('(.+)\((.+)\)', horse_name)
        if m != None:
            horse_name = m.groups()[0]
            country = m.groups()[1]
        else:
            country = 'JPN'

    def get_profile(self, soup):
        '''馬の基本情報を取得する'''

        # プロフィールテーブルの取得
        profile_table = soup.find_all('table', class_ = 'tbl-data-05 reset-mb-40')

        # 取得失敗時のログ出力
        if len(profile_table) == 0:
            self.logger.error('プロフィールテーブルが見つかりません')
            return
        elif len(profile_table) > 1:
            self.logger.warning('プロフィールテーブルが複数見つかりました。一番上のテーブルを取得対象にします')

        # テーブルの各セルのテキストを全て取得し、リスト化
        profiles = re.findall(r'<.+>(.+?)</.+>', mold.rm_charcode(str(profile_table[0])))

        # 取得失敗時のログ出力
        if len(profiles) == 0:
            self.logger.info('プロフィールテーブルのカラムが見つかりません')
            return

        # リンクのないデータの取得
        for index, profile in enumerate(profiles):
            # 最後の要素の場合は弾く
            if index == len(profiles) - 1 : break

            next_param = profiles[index + 1]

            if profile == '生年月日' and re.search('\d+/\d+/\d+', next_param) != None:
                birthday = next_param

            if profile == '毛色' and '毛' in next_param:
                hair_color = next_param.replace('毛', '')

            if profile == '産地' and '産' in next_param:
                hometown = next_param.replace('産', '')

            if profile == '市場取引' and index + 3 < len(profiles):
                seri_year = next_param.replace('年', '')
                seri_price = profiles[index + 2].replace('万円', '')

                seri_match = re.search('/seri/.+/(.+)/">(.+)</a>', str(profile_table[0]))
                if seri_match != None:
                    seri_id, seri_name = seri_match.groups()
                else:
                    seri_name = profiles[index + 3]

        # リンク付きデータの取得
        # 馬主
        owner_match = re.search('/horse/owner/(.+)/">(.+)</a>', str(profile_table[0]))
        if owner_match != None:
            owner_id, owner = owner_match.groups()

        # 調教師
        trainer_match = re.search('/horse/trainer/(.+)/">(.+)</a>(.+)</td>', str(profile_table[0]))
        if trainer_match != None:
            trainer_id, trainer, trainer_belong = trainer_match.groups()
            trainer_belong = mold.rm(trainer_belong).replace('（', '').replace('）', '')

        # 生産牧場
        farm_match = re.search('/breeder/(.+)/">(.+)</a>', str(profile_table[0]))
        if farm_match != None:
            farm_id, farm = farm_match.groups()

    def get_blood(self, soup):
        '''血統表情報を取得する'''

        # 血統表テーブルを取得
        blood_table = soup.find_all('table', class_ = 'tbl-pedigree-01 reset-mb-40')

        # 取得失敗時のログ出力
        if len(blood_table) == 0:
            self.logger.error('血統表テーブルが見つかりません')
            return
        elif len(blood_table) > 1:
            self.logger.warning('血統表テーブルが複数見つかりました。一番上のテーブルを取得対象にします')

        blood = blood_table[0]

        # 両親
        f_id, f_name = self.blood_match(blood.find('th', class_ = 'male'))
        m_id, m_name = self.blood_match(blood.find('th', class_ = 'female'))

        # 祖父
        ground_father = blood.find_all('td', class_ = 'male')
        ff_id, ff_name = self.blood_match(ground_father[0])
        mf_id, mf_name = self.blood_match(ground_father[1])

        # 祖母
        ground_mother = blood.find_all('td', class_ = 'female')
        fm_id, fm_name = self.blood_match(ground_mother[0])
        mm_id, mm_name = self.blood_match(ground_mother[1])

    def blood_match(self, frame):
        match = re.search('<a href="/horse/(.*)/">(.*)</a>', str(frame))
        if match != None:
            return match.groups()
        else:
            return ['', '']