def int_check(text, digit = None):
    '''int�Ѵ���ǽ���Υ����å� / �����������å�'''
    try:
        int(text)
        if digit != None:
            if len(str(text)) != digit:
                return False
        return True
    except:
        return False

