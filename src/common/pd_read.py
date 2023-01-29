import log
import pandas as pd
import time
import traceback

logger = log.Logger()

def get_table(URL, sleep_time = 0, retry_count = 0):
    '''テーブル取得のリトライ処理

         Args:
             URL(str) : 取得対象のURL
             sleep_time(int) : リトライまでのアイドルタイム(デフォルト : 3秒)
             retry_count(int) : 最大リトライ回数(デフォルト : 0回)

         Returns:
             tables(list[pandas.DataFrame, pandas.DataFrame, ...) : 取得したテーブルタグをDataFrame型に変換したリスト
             0 : テーブル未取得エラー(HTML内にテーブルタグが見つからない)
             -1 : その他のエラー(接続失敗など)
    '''

    for _ in range(retry_count + 1):
        try:
            return pd.read_html(URL)
        except ValueError as v:
            logger.error(v)
            logger.error(traceback.format_exc())
            return 0
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            if sleep_time != 0:
                time.sleep(sleep_time)
    else:
        return -1