### 簡単計算を行う共通関数 ###

def frame_no_culc(horse_num, horse_no):
    '''馬番と頭数から枠番を計算(18頭以内のみ対応可)
        TODO もう少しスマートにしたい

    Args:
        horse_num(int変換可能な型) : 出走頭数
        horse_no(int変換可能な型) : 対象馬の馬番

    Returns:
        frame_no(str) : 対象馬の枠番
    '''
    horse_no = int(horse_no)
    horse_num = int(horse_num)

    if horse_no == 1:
        return str(1)
    elif horse_num <= 8 or horse_no < horse_num * -1 + 18:
        return str(horse_no)
    elif horse_num <= 16:
        if horse_no <= 8:
            return str(min(8, horse_no) - int((horse_no - (horse_num * -1 + 16)) / 2))
        else:
            return str(int(8 - (horse_num - horse_no - 1) / 2))
    else:
        if horse_no >= 17:
            return str(8)
        elif horse_num == 18 and horse_no == 15:
            return str(7)
        else:
            return frame_no_culc(16, horse_no)