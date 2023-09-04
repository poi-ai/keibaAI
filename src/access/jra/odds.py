from base import Base
from .do_action import DoAction

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

o = Odds()
o.get_wakuren('pw153ou1004202303080120230903Z/F8')