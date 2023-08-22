import requests
import time
import traceback
from bs4 import BeautifulSoup
from base import Base

class Cron(Base):
    def __init__(self):
        super().__init__()

    def main(self):
        # 時間計測開始
        start_time = time.time()

        # 2023桜花賞のページへアクセス
        try:
            r = requests.get('https://www.jbis.or.jp/race/result/20230409/109/11/')
        except Exception as e:
            self.logger.error(f'HTML取得エラー\n{e}\n{traceback.format_exc()}')
            exit()

        # 時間計測終了
        elapsed_time = time.time() - start_time

        # レスポンスコードが200番台でない場合self.logger.error()でエラーログを出す
        if r.status_code < 200 or r.status_code >= 300:
            self.logger.error(f'レスポンスコードエラー: {r.status_code}')
            exit()

        soup = BeautifulSoup(r.content, 'lxml')

        # soupが空の場合self.logger.error()でエラーログを出す
        if soup is None or len(soup) == 0:
            self.logger.error('取得したHTMLが空')
            exit()

        self.logger.info(f'HTML取得に成功 実行時間: {elapsed_time:.2f}秒')

if __name__ == '__main__':
    c = Cron()
    c.main()