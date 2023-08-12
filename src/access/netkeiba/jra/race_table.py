import babaid
import culc
import gethtml
import mold
import re
import traceback
from base import Base

class RaceTable(Base):
    '''netkeibaから中央競馬の出走表を取得する'''
    def __init__(self,):
        super().__init__()

    def set(self, race_id, race_date = ''):
        self.race_id = race_id
        self.race_date = race_date

    def get(self):
        '''
        netkeibaから指定したレースIDの出走表を取得する

        Returns:
            race_info(dict) or None: レース情報
            horse_info(list[dict, dict]) or None: 出走馬情報
            bool: 実行結果

        '''
        try:
            self.logger.info(f'netkeibaから出走表ページのHTML取得処理開始 レースID: {self.race_id}')
            soup = self.get_soup()
            self.logger.info(f'netkeibaから出走表ページのHTML取得処理終了 レースID: {self.race_id}')
        except Exception as e:
            self.error_input('netkeiba出走表ページ取得処理でエラー', e, traceback.format_exc())
            return None, None, False

        try:
            self.logger.info(f'netkeiba出走表からのレース情報取得処理開始 レースID: {self.race_id}')
            race_info = self.get_race_info(soup)
            self.logger.info(f'netkeiba出走表からのレース情報取得処理終了 レースID: {self.race_id}')
        except Exception as e:
            self.error_input('netkeiba出走表からのレース情報取得処理でエラー', e, traceback.format_exc())
            return None, None, False

        try:
            self.logger.info(f'netkeibaの出走表からの出走馬情報取得処理開始 レースID: {self.race_id}')
            horse_info = self.get_horse_info(soup)
            self.logger.info(f'netkeibaの出走表からの出走馬情報取得処理終了 レースID: {self.race_id}')
        except Exception as e:
            self.error_input('netkeibaの出走表からの出走馬情報取得処理でエラー', e, traceback.format_exc())
            return None, None, False


        return race_info, horse_info, True

    def get_soup(self):
        '''出走表ページからHTMLを取得する'''
        url = f'https://race.netkeiba.com/race/shutuba_past.html?race_id={self.race_id}'
        return gethtml.soup(url)

    def get_race_info(self, soup):
        '''
        netkeibaの出走表からレース情報を取得する

        Args:
            soup(bs4.BeautifulSoup): 出走表ページのHTML

        Returns:
            race_info(dict) or None: レース情報
                TODO パラメータ書く
            bool: 実行結果

        '''
        race_info = {}

        # 日付が設定されていない場合はサイト内から取得
        if self.race_date == '':
            date_link = soup.find('dd', class_ = 'Active')
            m = re.search('kaisai_date=(\d+)', str(date_link))
            if m != None:
                self.race_date = race_info['race_date'] = m.groups()[0]

        # コース情報や状態を抽出
        race_data_01 = soup.find('div', class_ = 'RaceData01')
        race_data_list = mold.rm(race_data_01.text).split('/')

        # 当日公表データが少ない(=レース中止)の場合弾く
        if len(race_data_list) < 4:
            self.logger.info(f'{babaid.netkeiba(self.baba_id)}{self.race_no}R(race_id:{self.race_id})のレースデータが不足しているため記録を行いません')
            #self.logger.info(f'取得先URL:{url}')
            self.race_flg = False
            return None, False

        # 発走時刻取得
        race_info['race_time'] = race_data_list[0].replace('発走', '')

        # コース情報
        course = re.search('([芝|ダ|障])(\d+)m\((.*)\)', race_data_list[1])

        # 距離
        race_info['distance'] = course.groups()[1]

        # 平場/障害判定
        if course.groups()[0] == '障':
            race_info['race_type'] = '障'

            # 馬場と馬場状態
            baba = course.groups()[2]
            if '芝' in baba:
                if 'ダート' in baba:
                    race_info['baba'] = '芝ダ'
                    race_info['glass_condition'] = race_data_list[3].replace('馬場:', '')
                    if len(race_data_list) == 5:
                        race_info['dirt_condition'] = race_data_list[4].replace('馬場:', '')
                else:
                    race_info['baba'] = '芝'
                    race_info['glass_condition'] = race_data_list[3].replace('馬場:', '')
            else:
                race_info['baba'] = 'ダ'
                race_info['dirt_condition'] = race_data_list[3].replace('馬場:', '')

            # 右回り/左回り
            around = re.sub(r'[芝ダート]', '', baba)
            if len(around) != 0:
                race_info['in_out'] = around

        else:
            race_info['race_type'] = '平'

            # 馬場と馬場状態
            baba = course.groups()[0]
            race_info['baba'] = baba
            if baba == '芝':
                race_info['glass_condition'] = race_data_list[3].replace('馬場:', '')
            elif baba == 'ダ':
                race_info['dirt_condition'] = race_data_list[3].replace('馬場:', '')

            # 右/左、内/外、直線
            around = course.groups()[2]
            if around == '直線':
                race_info['around'] = '直'
            else:
                race_info['around'] = around[0]
                if len(around) != 1:
                    race_info['in_out'] = around[1:]

        # 天候
        race_info['weather'] = race_data_list[2].replace('天候:', '')

        # 出走条件等の抽出
        race_data_02 = soup.find('div', class_ = 'RaceData02')

        # 開催回/日・競馬場コード
        race_data_list = race_data_02.text.split('\n')
        race_info['hold_no'] = race_data_list[1].replace('回', '')
        race_info['baba_id'] = babaid.netkeiba(race_data_list[2])
        race_info['hold_date'] = race_data_list[3].replace('日目', '')

        # 出走条件(馬齢/クラス)
        race_info['require_age'] = mold.full_to_half(race_data_list[4]).replace('サラ系', '').replace('障害', '')
        race_info['race_class'] = mold.full_to_half(race_data_list[5])

        # レース名
        race_name = soup.find('div', class_ = 'RaceName')
        race_info['race_name'] = race_name.text.replace('\n', '')

        # CSSからクラスチェック、13はWIN5
        if 'Icon_GradeType2' in str(race_name):
            race_info['grade'] = 'GII'
        elif 'Icon_GradeType3' in str(race_name):
            race_info['grade'] = 'GIII'
        elif 'Icon_GradeType4' in str(race_name):
            race_info['grade'] = '重賞'
        elif 'Icon_GradeType5' in str(race_name):
            race_info['grade'] = 'OP'
        elif 'Icon_GradeType6' in str(race_name):
            race_info['grade'] = '1600万下'
        elif 'Icon_GradeType7' in str(race_name):
            race_info['grade'] = '1000万下'
        elif 'Icon_GradeType8' in str(race_name):
            race_info['grade'] = '900万下'
        elif 'Icon_GradeType9' in str(race_name):
            race_info['grade'] = '500万下'
        elif 'Icon_GradeType10' in str(race_name):
            race_info['grade'] = 'JGI'
        elif 'Icon_GradeType11' in str(race_name):
            race_info['grade'] = 'JGII'
        elif 'Icon_GradeType12' in str(race_name):
            race_info['grade'] = 'JGIII'
        elif 'Icon_GradeType15' in str(race_name):
            race_info['grade'] = 'L'
        elif 'Icon_GradeType16' in str(race_name):
            race_info['grade'] = '3勝'
        elif 'Icon_GradeType17' in str(race_name):
            race_info['grade'] = '2勝'
        elif 'Icon_GradeType18' in str(race_name):
            race_info['grade'] = '1勝'
        elif 'Icon_GradeType1' in str(race_name):
            race_info['grade'] = 'GI'

        # 待選、暫定処理としてグレードの末尾に付けておく
        if 'Icon_GradeType14' in str(race_name):
            race_info['grade'] += '待選'

        # 馬齢以外の出走条件
        require = race_data_list[7]

        # 国際/混合レース
        # 国際...外国産馬が出走可
        # 混合...日本調教外国産馬が出走可
        if '(国際)' in require:
            race_info['require_country'] = '国'
        elif '(混)' in require:
            race_info['require_country'] = '混'

        # 出走条件性別
        if '牡・牝' in require:
            race_info['require_gender'] = '牡牝'
        elif '牝' in require:
            race_info['require_gender'] = '牝'

        # 指定/特別指定
        #   マル指...特指以外の地方出走可
        #   カク指...地方騎手騎乗可
        # 特別指定...JRA認定地方レースの1着馬が出走可
        if '(指)' in require:
            race_info['require_local'] = 'マル指'
        elif '(特指)' in require:
            race_info['require_local'] = '特指'
        elif '指' in require:
            race_info['require_local'] = 'カク指'

        # 九州産馬限定戦・見習騎手限定戦
        if '九州産馬' in require:
            race_info['require_local'] = '1'

        # 見習騎手限定戦
        if '見習騎手' in require:
            race_info['require_beginner_jockey'] = '1'

        # 斤量条件[定量/馬齢/別定/ハンデ]
        race_info['load_kind'] = race_data_list[8]

        # 登録頭数
        self.regist_num = race_info['regist_num'] = race_data_list[9].replace('頭', '')

        # 出走頭数計算(登録頭数 - 取消・除外頭数)
        cancel_num = soup.find('td', class_ = 'Cancel_NoData')
        if cancel_num == None: cancel_num = []
        race_info['run_num'] = str(int(race_info['regist_num']) - len(cancel_num))

        # レース賞金
        prize = re.search('本賞金:(\d+),(\d+),(\d+),(\d+),(\d+)万円', race_data_list[11])
        race_info['first_prize'] = float(prize.groups()[0]) * 10
        race_info['second_prize'] = float(prize.groups()[1]) * 10
        race_info['third_prize'] = float(prize.groups()[2]) * 10
        race_info['fourth_prize'] = float(prize.groups()[3]) * 10
        race_info['fifth_prize'] = float(prize.groups()[4]) * 10


    def horse_info(self, soup):
        '''
        netkeibaの出走表から出走馬の情報を取得する

        Args:
            soup(bs4.BeautifulSoup): レース出走表ページのHTML

        Returns:
            horse_info_list(list[dict{], dict{}...]) or None: 各出走馬の情報
                TODO 各パラメータ書く
            bool: 実行結果

        '''
        horse_info_list = []

        # 各馬の情報取得
        fc = soup.select('div[class="fc"]')
        for i, info in enumerate(fc):
            horse_info = {}

            # レースID追加
            horse_info['race_id'] = self.race_id

            # 所属や馬名の書いてる枠
            horse_type = info.find('div', class_ = 'Horse02')

            # 外国産(所属)馬/地方所属馬判定
            if 'Icon_MaruChi' in str(horse_type):
                horse_info['belong'] = 'マル地'
            elif 'Icon_kakuChi' in str(horse_type):
                horse_info['belong'] = 'カク地'
            elif 'Icon_MaruGai' in str(horse_type):
                horse_info['country'] = 'マル外'
            elif 'Icon_KakuGai' in str(horse_type):
                horse_info['country'] = 'カク外'

            # ブリンカー有無
            if '<span class="Mark">B</span>' in str(horse_type):
                horse_info['blinker'] = '1'

            # netkeiba独自の競走馬ID/馬名
            m = re.search('db.netkeiba.com/horse/(\d+)" target="_blank">', str(horse_type))
            if m != None:
                horse_info['horse_id'] = m.groups()[0]
            else:
                self.logger.info(f'{babaid.netkeiba(self.baba_id)}{self.race_no}R(race_id:{self.race_id})の競走馬データが見つかりません')
                self.race_flg = False
                return

            # 馬名
            horse_name = mold.rm(horse_type.text)

            # 末尾にブリンカーマークがついていたら除去
            if horse_name.endswith('B'):
                horse_info['horse_name'] = horse_name[:len(horse_name) - 1]
            else:
                horse_info['horse_name'] = horse_name

            # 父名・母名・母父名
            horse_info['father'] = info.find('div', class_ = 'Horse01').text
            horse_info['mother'] = info.find('div', class_ = 'Horse03').text
            horse_info['grandfather'] = info.find('div', class_ = 'Horse04').text.replace('(', '').replace(')', '')

            # 調教師・調教師所属
            trainer = info.find('div', class_ = 'Horse05').text.split('・')
            horse_info['trainer_belong'] = trainer[0]
            horse_info['trainer'] = mold.rm(trainer[1])

            # netkeiba独自の調教師ID
            trainer_id = re.search('db.netkeiba.com/trainer/result/recent/(\d+)', str(info))
            if trainer_id != None:
                horse_info['trainer_id'] = str(trainer_id.groups()[0])

            # 出走間隔(週)
            blank = info.find('div', class_ = 'Horse06').text
            if blank == '連闘':
                horse_info['blank'] = '0'
            else:
                blank_week = re.search('中(\d+)週', blank)
                # 初出走判定
                if blank_week == None:
                    horse_info['blank'] = '-1'
                else:
                    horse_info['blank'] = blank_week.groups()[0]

            # 脚質(netkeiba独自)
            running_type = str(info.find('div', class_ = 'Horse06'))
            if 'horse_race_type00' in running_type:
                horse_info['running_type'] = '未'
            elif 'horse_race_type01' in running_type:
                horse_info['running_type'] = '逃'
            elif 'horse_race_type02' in running_type:
                horse_info['running_type'] = '先'
            elif 'horse_race_type03' in running_type:
                horse_info['running_type'] = '差'
            elif 'horse_race_type04' in running_type:
                horse_info['running_type'] = '追'
            elif 'horse_race_type05' in running_type:
                horse_info['running_type'] = '自在'

            # 馬体重
            weight = re.search('(\d+)kg\((.+)\)', info.find('div', class_ = 'Horse07').text)

            # 計不対応(前走計不は0と表示されるため対応不必要)
            if info.find('div', class_ = 'Horse07').text == '計不':
                horse_info['weight'] = '計不'
                horse_info['weight_change'] = '計不'

            if weight != None:
                horse_info['weight'] = weight.groups()[0]
                if str(weight.groups()[1]) == '前計不':
                    horse_info['weight_change'] = '前計不'
                else:
                    horse_info['weight_change'] = str(int(weight.groups()[1]))

            # 除外・取消馬は999kg(0)と表記される場合があるのでそれに対応
            if str(horse_info['weight']) == '999' and str(horse_info['weight_change']) == '0':
                horse_info['weight'] = ''
                horse_info['weight_change'] = ''

            # 馬番・枠番
            horse_info['horse_no'] = str(i + 1)
            horse_info['frame_no'] = culc.frame_no_culc(self.regist_num, int(i + 1))

            horse_info_list.append(horse_info)


        # 騎手等記載の隣の枠から情報取得
        jockeys = soup.find_all('td', class_ = 'Jockey')
        for i, info in enumerate(jockeys):

            # 最後の枠は説明用のサンプル枠なので飛ばす
            if i == len(jockeys) - 1:
                break

            horse_info = horse_info_list[i]

            # 性別・馬齢・毛色
            m = re.search('([牡|牝|セ])(\d+)(.+)', info.find('span', class_ = 'Barei').text)
            if m != None:
                horse_info['gender'] = m.groups()[0]
                horse_info['age'] = m.groups()[1]
                horse_info['hair_color'] = m.groups()[2]

            # 騎手名・netkeiba独自の騎手ID
            jockey = re.search('db.netkeiba.com/jockey/result/recent/(\d+)" target="_blank">(.+)</a>', str(info))
            if jockey != None:
                horse_info['jockey_id'] = str(jockey.groups()[0])

                # 騎手乗り代わりチェック
                if '<font color="red">' in jockey.groups()[1]:
                    horse_info['jockey'] = jockey.groups()[1].replace('<font color="red">', '').replace('</font>', '')
                    horse_info['jockey_change'] = '1'
                else:
                    horse_info['jockey'] = jockey.groups()[1]

            # 斤量
            load = re.search('<span>(\d+\d.\d+)</span>', str(info))
            if load != None:
                horse_info['load'] = load.groups()[0]

            horse_info_list[i] = horse_info

        return horse_info_list, True