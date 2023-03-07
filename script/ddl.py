import numpy as np
import math
import pandas as pd
import traceback

def main():
    # Excelファイル読み込み
    try:
        df = read_excel('create_ddl.xlsx', sheet_name='テーブル定義')
    except Exception as e:
        print('テーブル定義書が見つかりません')

    df.columns = [i for i in range(11)]

    # Excelから読み込んだパラメータかたCREATE文を組み立てる
    try:
        sql = assemble_sql(df)
    except Exception as e:
        print('\n'.join(['CREATE文組み立て処理でエラー', e, traceback.format_exc()]))

    # TODO .sqlへ出力処理
    # TODO Excelファイル名変更
    # TODO templateからファイルコピー

def read_excel():
    '''Excelファイルを読み込む'''
    return pd.read_excel('create_ddl.xlsx', sheet_name='テーブル定義')

def assemble_sql(df):
    '''読み込んだパラメータからCREATE文を組み立て'''

    # テーブル名取得
    table_name = df[2][0]

    if nan_check(table_name):
        print('テーブル名が未設定です')
        exit()

    ddl = f'CREATE TABLE {table_name} (\n'

    # パラメータの各項目を取得
    for index, row in enumerate(df.iterrows()):
        # 1行目はテーブル名、2行目はカラム名なのでパス
        if index == 0 or index == 1: continue

        # カラム名
        ddl += f' `{row[1][1]}` '

        # データ型/桁数
        if 'UNSIGNED' in row[1][2]:
            ddl += row[1][2].replace(' ', f'({row[1][3]}) ')
        else:
            ddl += f'{row[1][2]}'
            # 桁数
            if not nan_check(row[1][3]): ddl += f'({row[1][3]})'
        ddl += ' '

        # NOT NULL(必須)
        if row[1][4] == '○': ddl += 'NOT NULL '

        # UNIQUE(一意成約)
        if row[1][5] == '○': ddl += 'UNIQUE '

        # デフォルト値
        if not nan_check(row[1][8]): ddl += f'DEFAULT {row[1][8]} '

        # コメント
        if not nan_check(row[1][9]): ddl += f'COMMENT \'{row[1][9]}\''

        ddl += ',\n'

    # TODO 主キー・複合キー・外部キー処理
    # PRIMARY KEY (order_id, product_id),
    # FOREIGN KEY (product_id) REFERENCES products (product_id)

    # COLLATIONは「utf8mb4_general_ci」固定
    ddl += ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;'

    return ddl

def nan_check(text):
    '''Nanチェック、NanならTrueを返す'''
    if type(text) != float:
        return False
    if math.isnan(text):
        return True
    return False
