from base import Base
from .do_action import DoAction

class Odds(Base, DoAction):
    def __init__(self):
        super().__init__()

    def get_tanpuku(self, cname):
        '''
        ñ����ʣ�����å����������

        Args:
            cname(str): ���å��ڡ�����CNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_wakuren(self, cname):
        '''
        ��Ϣ�Υ��å����������

        Args:
            cname(str): ���å��ڡ�����CNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_umaren(self, cname):
        '''
        ��Ϣ�Υ��å����������

        Args:
            cname(str): ���å��ڡ�����CNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_wide(self, cname):
        '''
        �磻�ɤΥ��å����������

        Args:
            cname(str): ���å��ڡ�����CNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_umatan(self, cname):
        '''
        ��ñ�Υ��å����������

        Args:
            cname(str): ���å��ڡ�����CNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_trio(self, cname):
        '''
        ��Ϣʣ�Υ��å����������

        Args:
            cname(str): ���å��ڡ�����CNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

    def get_tirece(self, cname):
        '''
        ��Ϣñ�Υ��å����������

        Args:
            cname(str): ���å��ڡ�����CNAME

        Returns:

        '''
        soup = self.do_action(self.ODDS_BASE_URL, cname)

o = Odds()
o.get_wakuren('pw153ou1004202303080120230903Z/F8')