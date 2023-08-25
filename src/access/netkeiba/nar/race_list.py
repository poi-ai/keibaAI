import gethtml
import itertools
from base import Base

class RaceList(Base):
    '''netkeibaから指定した日付のレースIDを取得する'''

    def __init__(self):
        super().__init__()

    def get_race_id_list(self, date):
        '''
        指定日のレースID一覧を取得する

        Args:
            date(str): 対象年月日(yyyyMMdd) >= 20150225

        Returns:
            race_id_list(list): 指定した日付に実施された地方競馬のレースID一覧

        '''
        race_id_list = []

        # 同日開催でも競馬場ごとにページが異なり、そのページのIDパラメータに必要なため先に取得を行う
        hold_id_list = self.get_hold_id_list(date)

        # 競馬場ごとにレースIDの取得
        for hold_id in hold_id_list:
            URL = f'https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date={date}&kaisai_id={hold_id}'

            # HTMLの中からリンク取得
            soup = gethtml.soup(URL)
            links = soup.find_all('a')

            # リンクの中からレース結果ページのレースIDが書かれている部分のみ切り出す
            for link in links:
                race_url = link.get('href')
                if 'result' in race_url:
                    race_id_list.append(race_url[28:40])

        return race_id_list

    def get_hold_id_list(self, date):
        '''
        指定日の開催ID(=競馬場+日付毎に振られる一意のID)一覧を取得する

        Returns:
            hold_id_list(list): 指定した日付に実施された地方競馬の開催ID一覧

        '''
        # 開催IDが記載されているURL
        url = f'https://nar.netkeiba.com/top/race_list_sub.html?kaisai_date={date}'

        kaisai_id_list = []

        # HTMLからa属性を取得
        soup = gethtml.soup(url)
        li = soup.find_all('li')
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
