import json
import re

def full_to_half(text):
    '''全角から半角へ変換'''
    return text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

def half_to_full(text):
    '''半角から全角へ変換'''
    return text.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))

def rm(text):
    '''改行・空白を除去'''
    return text.replace('\n', '').replace('\r', '').replace('\xa0', '').replace(' ', '').replace('　', '')

def rm_nl(text):
    '''改行(New Line)コードを除去'''
    return text.replace('\n', '').replace('\r', '')

def rm_charcode(text):
    '''文字コードを除去'''
    return text.replace('\u3000', '').replace('\xa0', '')

def change_seconds(minutes_time):
    '''xx:xx.xフォーマットの時間をfloatで扱えるxx.x(秒)に変換する

    Args:
        minutes_time(str): ss:mm.x フォーマットの時間

    Returns:
        time(str): mm.x フォーマット(float変換可能な形)での時間
    '''
    separate_time = re.match('(\d+):(\d+).(\d+)', minutes_time)
    if separate_time != None:
        return str(int(separate_time.groups()[0]) * 60 + int(separate_time.groups()[1]) + float(separate_time.groups()[2]) * 0.1)
    else:
        return minutes_time

def json_to_dict(response_json, tidy_format = False):
    '''
    JSON型をdict型に変換する、引数指定すればインデント整形も行う

    Args:
        response_json(bytes): 変換したいJSON
        tidy_format(bool): 出力用にインデントを揃えるか

    Returns:
        parsed_response(dict): 変換後のdict

    '''
    parsed_response = json.loads(response_json)
    if tidy_format:
        tidy_dict(parsed_response)
    return parsed_response

def tidy_dict(target_dict):
    '''辞書型をインデント4で整形する'''
    return json.dumps(target_dict, indent = 4, ensure_ascii = False)