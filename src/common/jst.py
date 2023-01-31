from datetime import datetime, timedelta

'''日本時間を取得'''
def now():
    '''現在の時刻(JST)をdatetime型で返す'''
    return datetime.utcnow() + timedelta(hours=9)

def date():
    '''現在の日付(JST)をstr型[YYYYmmdd]で返す'''
    return now().strftime("%Y%m%d")

def time():
    '''現在の時刻(JST)をstr型[YYYYmmddHHMMSS]で返す'''
    return now().strftime("%Y%m%d%H%M%S")

def mtime():
    '''現在の時刻(JST)をstr型[YYYYmmddHHMM]で返す'''
    return now().strftime("%Y%m%d%H%M")

def year():
    '''現在の年(JST)をstr型[YYYY]で返す'''
    return str(now().year)

def month():
    '''現在の月(JST)をstr型[m(0埋めなし)]で返す'''
    return str(now().month)

def zmonth():
    '''現在の月(JST)をstr型[mm(0埋め)]で返す'''
    return str(now().month).zfill(2)

def day():
    '''現在の日(JST)をstr型[d(0埋めなし)]で返す'''
    return str(now().day)

def zday():
    '''現在の日(JST)をstr型[dd(0埋め)]で返す'''
    return str(now().day).zfill(2)

def hour():
    '''現在の時間(JST)をstr型[H(0埋めなし)]で返す'''
    return str(now().hour)

def minute():
    '''現在の分(JST)をstr型[M(0埋めなし)]で返す'''
    return str(now().minute)

def second():
    '''現在の秒(JST)をstr型[S(0埋めなし)]で返す'''
    return str(now().second)

def time_min(time1, time2):
    '''datetime型の値を比較し、古い(小さい)方をdatetime型で返す'''
    return datetime.strptime(min(time1.strftime("%Y%m%d%H%M%S"), time2.strftime("%Y%m%d%H%M%S")), "%Y%m%d%H%M%S")

def between_month(date1, date2):
    '''2つの日付間の年月を取得する'''

    # datetime型に変換
    start = datetime.strptime(min(date1, date2), "%Y%m%d")
    end = datetime.strptime(max(date1, date2), "%Y%m%d")

    # 2日付間の全日付を取得
    date_range = [start + timedelta(days = x) for x in range(0, (end - start).days + 1)]

    # 年月だけ文字列型に変換し、重複を削除する
    month_list = []
    for date in date_range:
        if date.strftime("%Y%m") not in month_list:
            month_list.append(date.strftime("%Y%m"))

    return month_list

def yesterday(date = date()):
    '''指定した一日前の日付をstr型(yyyyMMDD)で返す'''
    dt_date = datetime.strptime(date, '%Y%m%d')
    return datetime.strftime(dt_date - timedelta(1), '%Y%m%d')

def clock(date = now()):
    '''指定した時間をHH:MMフォーマットで返す'''
    return datetime.strftime(date, '%H:%M')

def change_format(value, before_format, after_format):
    '''時間を表すstr型のフォーマットを変更して返す'''
    return datetime.strftime(datetime.strptime(value, before_format), after_format)


