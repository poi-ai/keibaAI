import logger as lg

# エラー回避用ログインスタンス作成
logger = lg.Logger()

def netkeiba(str):
    '''netkeiba.comのDBで使用されている競馬場コードを変換するメソッド
       ばんえい競馬は「競馬場名+(ば)」、中央と地方両方行われていた競馬場では、
       地方を「競馬場名+(地)」で表記

    Args:
        str(str):競馬場名 あるいは 競馬場コード

    Returns:
        引数が競馬場名の場合は競馬場コード
        引数が競馬場コードの場合は競馬場名

    '''
    COURSE = {'札幌': '01', '函館': '02', '福島': '03', '新潟': '04', '東京': '05',\
              '中山': '06', '中京': '07', '京都': '08', '阪神': '09', '小倉': '10','門別': '30',\
              '北見': '31', '岩見沢': '32', '帯広': '33', '旭川': '34', '盛岡': '35',\
              '水沢': '36', '上山': '37', '三条': '38', '足利': '39', '宇都宮': '40',\
              '高崎': '41', '浦和': '42', '船橋': '43', '大井': '44', '川崎': '45',\
              '金沢': '46', '笠松': '47', '名古屋': '48', '紀三井寺': '49', '園田': '50',\
              '姫路': '51', '益田': '52', '福山': '53', '高知': '54', '佐賀': '55',\
              '荒尾': '56', '中津': '57', '札幌(地)': '58', '函館(地)': '59', '新潟(地)': '60',\
              '中京(地)': '61', '春木': '62', '北見(ば)': '63', '岩見沢(ば)': '64', '帯広(ば)': '65',\
              '旭川(ば)': '66'}

    return check(str, COURSE, 'netkeiba')

def rakuten(str):
    '''楽天競馬のDBで使用されている競馬場コードを変換するメソッド
       ばんえい競馬は「競馬場名+ば」、中央と地方両方行われていた競馬場では、
       地方を「競馬場名+地」で表記

    Args:
        str(str):競馬場名 あるいは 競馬場コード

    Returns:
        引数が競馬場名の場合は競馬場コード
        引数が競馬場コードの場合は競馬場名

    '''
    COURSE = {'北見ば': '01', '岩見沢ば': '02', '帯広ば': '03', '旭川ば': '04', '岩見沢': '05',\
              '帯広': '06', '旭川': '07', '札幌地': '08', '函館地': '09', '盛岡': '10',\
              '水沢': '11', '上沢': '12', '新潟地': '13', '三条': '14', '足利': '15',\
              '宇都宮': '16', '高崎': '17', '浦和': '18', '船橋': '19', '大井': '20',\
              '川崎': '21', '金沢': '22', '笠松': '23', '名古屋': '24', '中京地': '25',\
              '紀三井寺': '26', '園田': '27', '姫路': '28', '益田': '29', '福山': '30',\
              '高知': '31', '佐賀': '32', '荒尾': '33', '中津': '34', '春木': '35',\
              '門別': '36'}

    return check(str, COURSE, '楽天競馬')

def keibago(str):
    '''keiba.go.jpで使用されている競馬場コードを変換するメソッド

    Args:
        str(str):競馬場名 あるいは 競馬場コード

    Returns:
        引数が競馬場名の場合は競馬場コード
        引数が競馬場コードの場合は競馬場名

    '''
    COURSE = {'北見ば': '1', '岩見ば': '2', '帯広ば': '3', '旭川ば': '4',\
              '岩見沢': '5', '帯広': '6', '旭川': '7', '札幌': '8', '函館': '9',\
              '盛岡': '10', '水沢': '11', '上山': '12', '新潟': '13', '三条': '14',\
              '足利': '15', '宇都宮': '16', '高崎': '17', '浦和': '18', '船橋': '19',\
              '大井': '20', '川崎': '21', '金沢': '22', '笠松': '23', '名古屋': '24',\
              '中京': '25', '紀三井寺': '26', '園田': '27', '姫路': '28', '益田': '29',\
              '福山': '30', '高知': '31', '佐賀': '32', '荒尾': '33', '中津': '34', '門別': '36'}

    return check(str, COURSE, 'keibago')

def jra(str):
    '''JRAで使用されている競馬場コードを変換するメソッド

    Args:
        str(str):競馬場名 あるいは 競馬場コード

    Returns:
        引数が競馬場名の場合は競馬場コード
        引数が競馬場コードの場合は競馬場名

    '''
    COURSE = {'札幌': '01', '函館': '02', '福島': '03', '新潟': '04', '東京': '05',\
              '中山': '06', '中京': '07', '京都': '08', '阪神': '09', '小倉': '10'}

    return check(str, COURSE, 'JRA')

def check(str, COURSE, kind):
    if str in COURSE:
        return COURSE[str]

    if str in COURSE.values():
        return [i for i, v in COURSE.items() if v == str][0]

    logger.error(f'{kind}の競馬場コード変換に失敗しました')
    raise