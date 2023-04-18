import csv
import os
import traceback
from jbis import race_list, race_result, racing_calendar

def export_dict_to_csv(data_dict, file_name):
    '''dict型のデータをCSVファイルに出力する

    Args:
        data_dict (dict): CSVファイルに書き込むdict型のデータ
        file_name (str): 出力先のCSVファイル名

    Returns:
        bool: ファイル書き込みが正常に完了したかどうか
        str: ファイル書き込み時に発生したエラーメッセージ
    '''
    try:
        # ファイルが既に存在するか確認
        file_exists = os.path.isfile(file_name)

        # ファイルをUTF-8で開き、追記モードで書き込む
        with open(file_name, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)

            # ファイルが存在しない場合は、キーをファイルの最初の行に書き込む
            if not file_exists:
                writer.writerow(data_dict.keys())

            # 値をファイルに書き込む
            writer.writerow(data_dict.values())

        # ファイル書き込みが正常に完了したことを返す
        return True, ''

    except Exception as e:
        # ファイル書き込み時にエラーが発生したこととエラーメッセージを返す
        return False, str(e)

OLDEST_DATE = '20200101'
LATEST_DATE = '20230401'

c = racing_calendar.Calendar(OLDEST_DATE, LATEST_DATE)

hold_list = c.get()

for hold in hold_list:
    race_date, course_id = hold

    rl = race_list.RaceList(race_date, course_id)

    link_type, race_no_list = rl.main()

    for race_no in race_no_list:
        rr = race_result.RaceResult(race_date, course_id, race_no)

        soup, exist = rr.get_soup()

        # レース概要を取得
        try:
           race_result_info, result = rr.get_race_summary(soup)
        except Exception as e:
            rr.error_output('レース概要取得処理でエラー', e, traceback.format_exc())
            continue

        if result:
            export_dict_to_csv(race_result_info, 'summary.csv')

        # レース結果情報を取得
        try:
            race_result_info_list, result = rr.get_horse_result(soup)
        except Exception as e:
            rr.error_output('出走馬結果取得処理でエラー', e, traceback.format_exc())
            continue

        if result:
            for info in race_result_info_list:
                export_dict_to_csv(info, 'horse_result.csv')

        # ラップタイムを取得
        try:
            lap_info_list = rr.get_lap(soup)
        except Exception as e:
            rr.error_output('ラップタイム取得処理でエラー', e, traceback.format_exc())
            continue

        if lap_info_list != None:
            for info in lap_info_list:
                export_dict_to_csv(info, 'lap_time.csv')

        # コーナー通過順位を取得
        try:
            corner_rank = rr.get_corner_rank(soup)
        except Exception as e:
            rr.error_output('コーナー通過順位取得処理でエラー', e, traceback.format_exc())
            continue

        if corner_rank != None:
            export_dict_to_csv(corner_rank, 'corner_rank.csv')

    rr.logger.info(f'race_date: {race_date}、 course_id: {course_id} 終了')

