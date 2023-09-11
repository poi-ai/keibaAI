from base import Base
from do_action import DoAction

class Odds(Base, DoAction):
    def __init__(self):
        super().__init__()

    def get_tanpuku(self, cname):
        '''
        単勝・複勝オッズを取得する

        Args:
            cname(str): オッズページのCNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_wakuren(self, cname):
        '''
        枠連のオッズを取得する

        Args:
            cname(str): オッズページのCNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_umaren(self, cname):
        '''
        馬連のオッズを取得する

        Args:
            cname(str): オッズページのCNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_wide(self, cname):
        '''
        ワイドのオッズを取得する

        Args:
            cname(str): オッズページのCNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_umatan(self, cname):
        '''
        馬単のオッズを取得する

        Args:
            cname(str): オッズページのCNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_trio(self, cname):
        '''
        三連複のオッズを取得する

        Args:
            cname(str): オッズページのCNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_tirece(self, cname):
        '''
        三連単のオッズを取得する

        Args:
            cname(str): オッズページのCNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def judge_page_type(self, cname):
        '''
        指定したCNAMEのページがどの券種のページか判断する

        Args:
            cname(str): オッズページのCNAME

        Returns:
            page_type(str): どの種別のページか
                tanpuku: 単複、wakuren: 枠連、umaren: 馬連、wide: ワイド、
                umatan: 馬単、trio: 三連複、tirece: 三連単、unknown: 不明

        '''
        # HTML取得
        soup = self.do_action(self.ODDS_BASE_URL, cname)

        # ボタンをアクティブにする(=へこませる)ためのCSSを呼ぶクラスを持つ項目を取得
        current_list = soup.find_all('li', class_ = 'current')

        # 一つずつ見ていき当てはまるものを返す
        for current in current_list:
            c = current.text
            if '単勝・複勝' in c:
                return 'tanpuku'
            elif '枠連' in c:
                return 'wakuren'
            elif '馬連' in c:
                return 'wide'
            elif '馬単' in c:
                return 'umatan'
            elif 'ワイド' in c:
                return 'wide'
            elif '3連複' in c:
                return 'trio'
            elif '3連単' in c:
                return 'tirece'
        # どれも一致しなかった場合
        return 'unknown'

o = Odds()
print(o.judge_page_type('pw151ou1004202303080120230903Z/F0'))
