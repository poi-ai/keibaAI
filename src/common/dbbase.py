import inspect
import pymysql
import dbconfig
from base import Base
from pathlib import Path

class DbBase(Base):
    '''データベース接続/操作を簡略化するための共通クラス'''

    def __init__(self):
        super().__init__(Path(inspect.stack()[1].filename).stem)
        self.conn = self.connect()
        self.conn.autocommit(True)
        self.transaction_flag = True

    def connect(self):
        '''データベースへの接続'''
        return  pymysql.connect(
            host = dbconfig.HOST,
            user = dbconfig.USER,
            password = dbconfig.PASSWORD,
            db = dbconfig.DB
        )

    def start_transaction(self):
        '''トランザクション開始'''
        self.logger.info('トランザクション開始')
        self.conn.autocommit(False)
        self.transaction_flag = True

    def end_transaction(self):
        '''トランザクション終了'''
        self.logger.info('トランザクション終了')
        if self.transaction_flag:
            self.commit()
        else:
            self.rollback()
        self.conn.autocommit(True)

    def commit(self):
        '''コミット'''
        try:
            self.conn.commit()
        except Exception as e:
            self.logger.error('データベースコミット処理でエラー')
            self.logger.error(str(e))
            self.rollback()
            return

    def rollback(self):
        '''ロールバック'''
        try:
            self.conn.rollback()
        except Exception as e:
            self.logger.error('ロールバック処理でエラー')
            self.logger.error(str(e))
            return

    def execute(self, query):
        '''クエリ実行'''
        try:
            with self.conn.cursor() as cursor:
                self.logger.info(f'クエリ実行：{query}')
                cursor.execute(query)
        except Exception as e:
            self.logger.error('データベースクエリ実行でエラー')
            self.logger.error(str(e))
            return