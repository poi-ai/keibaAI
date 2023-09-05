from execbase import ExecBase

class Odds(ExecBase):
    '''現在のオッズを取得する'''

    def __init__(self):
        super().__init__()

    def set(self, association = 1, ticket_type = 1):
        '''
        取得条件を設定する

        Args:
            association(str or int): 対象
                1: 中央のみ、0: 中央+地方、-1: 地方のみ
            ticket_type(list or 1): 取得する券種
                1(str or int): 全て
                or
                list[]: 下記の中から必要な券種のみ要素として載せる
                    tanpuku: 単複、wakuren: 枠連、umaren: 馬連、wide: ワイド、
                    umatan: 馬単、trio: 三連複、tirece: 三連単
        '''
        # TODO バリデーションチェック

        self.association = association
        self.ticket_type = ticket_type

    def main():
        pass
