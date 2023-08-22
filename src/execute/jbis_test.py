import csv
import os
import traceback
from execbase import ExecBase

class JbisTest(ExecBase):
    def __init__(self):
        super().__init__()

    def main(self):
        OLDEST_DATE = '20230320'
        LATEST_DATE = '20230401'

        calendar = self.access.jbis.racing_calendar
        calendar.set(OLDEST_DATE, LATEST_DATE)

        hold_list = calendar.get()

        for hold in hold_list:
            race_date, course_id = hold

            race_list = self.access.jbis.race_list
            race_list.set(race_date, course_id)

            link_type, race_no_list = race_list.main()

            for race_no in race_no_list:
                race_result = self.access.jbis.race_result
                race_result.set(race_date, course_id, race_no)

                soup, exist = race_result.get_soup()

                # レース概要を取得
                try:
                    race_result_info, result = race_result.get_race_summary(soup)
                except Exception as e:
                    self.error_output('レース概要取得処理でエラー', e, traceback.format_exc())
                    continue

                if result:
                    self.export_dict_to_csv(race_result_info, 'summary.csv')

                # レース結果情報を取得
                try:
                    race_result_info_list, result = race_result.get_horse_result(soup)
                except Exception as e:
                    race_list.error_output('出走馬結果取得処理でエラー', e, traceback.format_exc())
                    continue

                if result:
                    for info in race_result_info_list:
                        self.export_dict_to_csv(info, 'horse_result.csv')

                # ラップタイムを取得
                try:
                    lap_info_list = race_result.get_lap(soup)
                except Exception as e:
                    self.error_output('ラップタイム取得処理でエラー', e, traceback.format_exc())
                    continue

                if lap_info_list != None:
                    for info in lap_info_list:
                        self.export_dict_to_csv(info, 'lap_time.csv')

                # コーナー通過順位を取得
                try:
                    corner_rank = race_result.get_corner_rank(soup)
                except Exception as e:
                    race_result.error_output('コーナー通過順位取得処理でエラー', e, traceback.format_exc())
                    continue

                if corner_rank != None:
                    self.export_dict_to_csv(corner_rank, 'corner_rank.csv')

            self.logger.info(f'race_date: {race_date}、 course_id: {course_id} 終了')

    def export_dict_to_csv(self, data_dict, file_name):
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
            file_exists = os.path.isfile(os.path.join('csv', file_name))

            # ファイルをUTF-8で開き、追記モードで書き込む
            with open(os.path.join('csv', file_name), 'a', newline='', encoding='utf-8') as csv_file:
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

