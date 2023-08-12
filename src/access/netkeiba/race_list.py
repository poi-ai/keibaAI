import gethtml
import itertools
import traceback
from base import Base

class RaceList(Base):
    '''netkeibaのレースリストからレースIDを取得する'''

    def __init__(self):
        '''
        取得対象となる条件を指定

        Args:
            date(str): 対象年月日(yyyyMMdd) JRA >= 20070728, NAR >= 20150225
            association(str): 対象の開催協会(JRA or NAR)

        '''
        super().__init__()

    def set(self, date, association):
        self.date = date
        self.association = association

    def get(self):
        '''
        指定条件に合致するレースID一覧を取得する TODO 後で移植

        Returns:
            race_id_list(list) or None: レースID一覧
            bool: 実行結果

        '''
        if self.association.upper() == 'JRA':
            try:
                # 中央競馬のレースID一覧を取得
                self.logger.info(f'中央競馬レースID一覧取得開始 対象日: {self.date}')
                race_id_list = self.get_race_id_list()
                self.logger.info(f'中央競馬レースID一覧取得終了 対象日: {self.date}')
            except Exception as e:
                self.error_input('中央競馬レースID一覧取得処理でエラー', e, traceback.format_exc())
                return None, False
        elif self.association.upper() == 'NAR':
            try:
                # 地方競馬の開催ID一覧を取得
                self.logger.info(f'地方競馬開催ID一覧取得開始 対象日: {self.date}')
                hold_id = self.get_nar_hold_id_list()
                self.logger.info(f'地方競馬開催ID一覧取得終了 対象日: {self.date}')
            except Exception as e:
                self.error_input('地方競馬開催ID一覧取得処理でエラー', e, traceback.format_exc())
                return None, False

            try:
                # 地方競馬のレースID一覧を取得
                # 引数は開催IDリストの1番目だけでよい
                self.logger.info(f'地方競馬レースID一覧取得開始 対象日: {self.date}')
                race_id_list = self.get_race_id_list(hold_id[0])
                self.logger.info(f'地方競馬レースID一覧取得終了 対象日: {self.date}')
            except Exception as e:
                self.error_input('地方競馬レースID一覧取得処理でエラー', e, traceback.format_exc())
                return None, False
        else:
            self.error_input('指定した開催協会が存在しません')
            raise

        return race_id_list, True

    def get_race_id_list(self, hold_id = None):
        '''
        指定日/指定協会のレースID一覧を取得する

        Args:
            hold_id(str): 開催ID(=競馬場+日付毎に振られる一意のID)[地方のみ必須]

        Returns:
            race_id_list(list): 指定した日付に実施された中央競馬のレースID一覧

        '''
        if self.association.upper() == 'JRA':
            URL = f'https://race.netkeiba.com/top/race_list_sub.html?kaisai_date={self.date}'
        elif self.association.upper() == 'NAR':
            URL = f'https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date={self.date}&kaisai_id={hold_id}'

        race_id_list = []

        # HTML取得
        soup = gethtml.soup(URL)

        # HTMLの中からリンク取得
        links = soup.find_all('a')

        for link in links:
            race_url = link.get('href')
            # リンクの中からレース結果ページのみ取得し、レースIDを切り出す
            if 'result' in race_url:
                race_id_list.append(race_url[28:40])

        race_id_list

    def get_nar_hold_id_list(self):
        '''
        指定日の地方競馬の開催ID(=競馬場+日付毎に振られる一意のID)一覧を取得する

       Returns:
            hold_id_list(list): 指定した日付に実施された中央競馬の開催ID一覧

        '''
        # 開催IDが記載されているURL
        url = f'https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date={self.date}'

        kaisai_id_list = []

        # HTML取得
        soup = gethtml.soup(url)
        # 開催IDのリンクはli属性内にあるのでliを取得
        li = soup.find_all('li')

        # li属性内のa属性を取得

        links = [link.find_all('a') for link in li]
        # 一元化
        links = list(itertools.chain.from_iterable(links))

        # a属性から開催IDのリンクがあるURLを抽出
        for link in links:
            hold_url = link.get('href')
            # レース結果ページのみ取得しその中からレースIDを切り出す
            if 'kaisai_id' in hold_url:
                kaisai_id_list.append(hold_url[11:21])

        return kaisai_id_list