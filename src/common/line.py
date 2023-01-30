import config
import json
import log
import requests

logger = log.Logger()

def send(message, separate_no = 1):
    ''' LINEにメッセージを送信する
        送信にはconfig.py.LINE_TOKENにLINE Notice APIの
        APIトークンコードが記載されている必要がある(必須ではない)

    Args:
        message(str) : LINE送信するメッセージ内容
    '''
    # 10000字以上送ったらもうそれ以上送らない
    if separate_no > 10:
        logger.info('LINE Notifyでの送信メッセージが10000字を超えました')
        return

    # 設定ファイルからトークン取得
    try:
        token = config.LINE_TOKEN
    except AttributeError as e:
        return

    # 空なら何もしない
    if token == '':
        return

    # ヘッダー設定
    headers = {'Authorization': f'Bearer {token}'}

    # メッセージが1000文字(上限)を超えていたら分割して送る
    unsent_message = ''
    if len(message) > 999:
        unsent_message = message[1000:]
        message = message[:1000]

    # メッセージ設定
    data = {'message': f'{message}'}

    # メッセージ送信
    try:
        r = requests.post('https://notify-api.line.me/api/notify', headers = headers, data = data)
    except Exception as e:
        logger.error('LINE Notify APIでのメッセージ送信に失敗しました')
        logger.error(e)
        return

    if r.status_code != 200:
        logger.error('LINE Notify APIでエラーが発生しました')
        logger.error('ステータスコード：' + r.status_code)
        try:
            logger.error('エラー内容：' + json.dumps(json.loads(r.content), indent=2))
        except Exception as e:
            logger.error(e)
        return False

    # 未送信文字が残っていれば送信
    if unsent_message != '':
        send(unsent_message, separate_no + 1)
