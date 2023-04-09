import requests
import time
from bs4 import BeautifulSoup

def soup(URL):
    '''指定したURLからHTMLタグをスクレイピングするメソッド。
       意図せず高頻度アクセスを行ってしまうことを防ぐために
       requests.get()を行う場合は必ずこのメソッドを経由してアクセスを行う

    Args:
        URL(str):抽出対象のURL

    Retuens:
        soup(bs4.BeautifulSoup):抽出したHTMLタグ

    '''
    time.sleep(2)
    r = requests.get(URL)
    return BeautifulSoup(r.content, 'lxml')