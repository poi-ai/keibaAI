import config
import log
import requests

logger = log.Logger()
logger.set()

def send(message, separate_no = 1):
    ''' LINEにメッセージを送信する
        送信にはsettings.pyの「LINE_TOKEN」にLINE Noticeの
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
        logger.error('LINE Noticeでのメッセージ送信に失敗しました')
        return

    # TODO 送信失敗時の処理を書く(レスポンスコードから)

    # 未送信文字が残っていれば送信
    if unsent_message != '':
        send(unsent_message, separate_no + 1)
