import time
import re
import requests
from bs4 import BeautifulSoup

class DoAction:
    # オッズ関連ページのベースURL
    ODDS_BASE_URL = 'https://www.jra.go.jp/JRADB/accessO.html'
    # 出馬表関連ページのベースURL
    RACE_BASE_URL = 'https://www.jra.go.jp/JRADB/accessD.html'

    def do_action(self, url, cname):
        '''
        URL+CNAMEパラメータを持つPOSTリクエストを送り、HTML情報を取得する
        JRAの特殊なページ遷移方法

        Args:
            url(str): ベースになるURLs
            cname(str): CNAMEパラメータ

        Returns:
            soup(bs4.BeautifulSoup): 受け取ったHTML
        '''
        time.sleep(2)
        r = requests.post(url, data = {'cname': cname})
        # 文字化け対策(取得したHTMLから文字コードを推測して挿入)
        r.encoding = r.apparent_encoding
        return BeautifulSoup(r.text, 'lxml')

    def extract_param(self, html):
        '''
        HTMLからdo_actionの第二引数を抽出する

        Args:
            html(str): 抽出元のHTMLコード

        Returns:
            list[str]: 抽出した第二引数のリスト
        '''
        return [match.group(1) for match in re.finditer('access.\.html\', \'(\w+/\w+)', str(html))]
