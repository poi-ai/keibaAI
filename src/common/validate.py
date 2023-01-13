def int_check(text, digit = None):
    '''int変換可能かのチェック / 指定桁数チェック'''
    try:
        int(text)
        if digit != None:
            if len(str(text)) != digit:
                return False
        return True
    except:
        return False

