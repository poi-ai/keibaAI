import dbconfig
import inspect
import pymysql
import traceback
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
            self.error_output('コミット処理でエラー', e, traceback.format_exc())
            self.rollback()
            return

    def rollback(self):
        '''ロールバック'''
        try:
            self.conn.rollback()
        except Exception as e:
            self.error_output('ロールバック処理でエラー', e, traceback.format_exc())
            return

    def execute(self, query):
        '''クエリ実行'''
        try:
            with self.conn.cursor() as cursor:
                self.logger.info(f'クエリ実行：{query}')
                cursor.execute(query)
        except Exception as e:
            self.error_output('クエリ実行でエラー', e, traceback.format_exc())
            return

    def insert_df(self, df, table_name, complete_flg = False):
        '''DataFrame型のデータをDBに出力する

        Args:
           df(pandas.DataFrame) : DBに出力するデータ
           table_name(str) : 出力先のテーブル名
           complete_flg(bool) : 全レコード追加に成功した場合のみコミットするか

        Return:
           result(bool) : レコード追加の結果
           failed_df(pandas.dataframe) : 追加に失敗したレコード

        '''
        # 空ならそのまま返す
        if len(df) == 0: return

        # 返す用のdfをコピー
        result_df = df
        # 実行結果フラグ
        result_flag = True

        cursor = self.conn.cursor()

        cols = ', '.join([f'`{col}`' for col in df.columns])
        vals = ', '.join([f'%({col})s' for col in df.columns])

        # 一行抜き出してINSERT文実行
        for row_num, row in df.iterrows():
            try:
                sql = f'INSERT INTO {table_name} ({cols}) VALUES ({vals})'
                cursor.execute(sql, row.to_dict())
                if not complete_flg:
                    self.commit()
                result_df.drop(result_df.index[row_num])
            except Exception as e:
                self.error_output('DataFrameのINSERT処理でエラー', e, traceback.format_exc())
                self.rollback()
                result_flag = False
                if complete_flg:
                    break

        cursor.close()

        if complete_flg and result_flag:
            self.commit()

        return result_flag, result_df

        # TODO テスト 1.正常パターン 2.フラグON1行だけ失敗 3.フラグOFF1行だけ失敗

