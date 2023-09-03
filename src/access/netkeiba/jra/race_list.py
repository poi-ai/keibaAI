import gethtml
import traceback
from base import Base

class RaceList(Base):
    '''netkeibaから指定した日付のレースIDを取得する'''

    def __init__(self):
        super().__init__()

    def get_race_id_list(self, date):
        '''
        指定日のレースID一覧を取得する

        Args:
            date(str): 対象年月日(yyyyMMdd) >= 20070728

        Returns:
            race_id_list(list): 指定した日付に実施された中央競馬のレースID一覧

        '''
        URL = f'https://race.netkeiba.com/top/race_list_sub.html?kaisai_date={date}'

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

        return race_id_list
