import log

# エラー回避用ログインスタンス作成
logger = log.Logger()

def netkeiba(str):
    '''netkeiba.comで使用されている競馬場コードを変換するメソッド
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
              '水沢': '11', '上山': '12', '新潟地': '13', '三条': '14', '足利': '15',\
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

def jbis(str):
    '''JBISで使用されている競馬場コードを変換するメソッド

    Args:
        str(str):競馬場名 あるいは 競馬場コード

    Returns:
        引数が競馬場名の場合は競馬場コード
        引数が競馬場コードの場合は競馬場名
    '''
    COURSE = {'札幌': '101', '函館': '102', '福島': '103', '新潟': '104', '東京': '105',\
              '中山': '106', '中京': '107', '京都': '108', '阪神': '109', '小倉': '110',\
              '北見': '201', '岩見沢': '205', '帯広': '206', '旭川': '207', '札幌(地)': '208',\
              '函館(地)': '209', '盛岡': '210', '水沢': '211', '上沢': '212', '新潟(地)': '213',\
              '三条': '214', '足利': '215', '宇都宮': '216', '高崎': '217', '浦和': '218',
              '船橋': '219', '大井': '220', '川崎': '221', '金沢': '222', '笠松': '223',\
              '名古屋': '224', '中京(地)': '225', '紀三井寺': '226', '園田': '227', '姫路': '228',\
              '益田': '229', '福山': '230', '高知': '231', '佐賀': '232', '荒尾': '233',\
              '中津': '234', '春木': '235', '門別': '236'}

    return check(str, COURSE, 'JBIS')


def netkeiba_to_rakuten(babacode):
    '''netkeiba独自競馬場コードを楽天独自競馬場コードへ変換する
       北見は楽天に競馬場データが存在しないため変換できない

    Args:
        babacode(str):netkeiba独自競馬場コード

    Returns:
        楽天競馬独自競馬場コード

    '''

    COURSE = {'63': '01', '64': '02', '65': '03', '66': '04', '32': '05',\
              '33': '06', '34': '07', '58': '08', '59': '09', '35': '10',\
              '36': '11', '37': '12', '60': '13', '38': '14', '39': '15',\
              '40': '16', '41': '17', '42': '18', '43': '19', '44': '20',\
              '45': '21', '46': '22', '47': '23', '48': '24', '61': '25',\
              '49': '26', '50': '27', '51': '28', '52': '29', '53': '30',\
              '54': '31', '55': '32', '56': '33', '57': '34', '62': '35',\
              '30': '36'}

    return COURSE[babacode]

def rakuten_to_netkeiba(babacode):
    '''楽天競馬独自競馬場コードをnetkeiba独自競馬場コードへ変換する
    Args:
        babacode(str):楽天競馬独自競馬場コード

    Returns:
        netkeiba独自競馬場コード

    '''

    COURSE = {'36': '30', '05': '32', '06': '33', '07': '34', '10': '35',\
            '11': '36', '12': '37', '14': '38', '15': '39', '16': '40',\
            '17': '41', '18': '42', '19': '43', '20': '44', '21': '45',\
            '22': '46', '23': '47', '24': '48', '26': '49', '27': '50',\
            '28': '51', '29': '52', '30': '53', '31': '54', '32': '55',\
            '33': '56', '34': '57', '08': '58', '09': '59', '13': '60',\
            '25': '61', '35': '62', '01': '63', '02': '64', '03': '65',\
            '04': '66'}

    return COURSE[babacode]

def check(str, COURSE, kind):
    if str in COURSE:
        return COURSE[str]

    if str in COURSE.values():
        return [i for i, v in COURSE.items() if v == str][0]

    logger.error(f'{kind}の競馬場コード変換に失敗しました')
    raise