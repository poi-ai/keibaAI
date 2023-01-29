# Google Spread Sheet(スプレッドシート)へ出力するための共通ファイル
# 処理が煩雑になる上に、既存のスプレッドシートの取得周りの処理の自由度が低いためボツに
# いつか使うかもしれないので一応残しておく

'''
import gspread
import gspread_dataframe as gd
import os
import pandas as pd
from google.oauth2.service_account import Credentials

def write_spread_sheet(df, month, header=None):
    ''''''
       スプレッドシートにデータを書き込む。
       実行にはGoogle DriveとスプレッドシートのAPIを
       使用できる資格情報を書いたkeibaAI.jsonと、
       スプレッドシートIDを記載したSheetID.csvが必要。

    Args:
        df(pandas.DataFrame):スプレッドシートに書き込むデータ
        month(int):レース年月をyyyymmのint型で書き込むシートを指定
        header(list or pandas.DataFrame):スプレッドシートの1行目に書き込むヘッダ名を指定

    ''''''
    # スプレッドシートIDが記載されているCSVの取得
    df_id = pd.read_csv(os.path.dirname(__file__) + '/SheetID.csv')

    # スプレッドシートIDの設定
    target_sheet = df_id[df_id['month'] == month].reset_index()
    SPREADSHEET_KEY = target_sheet['id'][0]

    # スコープの設定
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

    # JSONファイルから資格情報の取得
    credentials = Credentials.from_service_account_file(os.path.dirname(__file__) + '/keibaAI.json', scopes=SCOPE)
    gc = gspread.authorize(credentials)

    # スプレッドシート情報の取得
    worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet('シート1')

    # 最終行の取得
    last_index = len(worksheet.col_values(1))

    # 新しいスプレッドシートに書き込む場合、先にヘッダー(カラム名)を書き込み
    if last_index + 1 == 1:
        if type(header) is list:
            df_header = pd.DataFrame(columns=header)
            gd.set_with_dataframe(worksheet, df_header, row = 1)
            last_index += 1
        elif type(header) is pd.DataFrame:
            df_header = header[:0]
            gd.set_with_dataframe(worksheet, df_header, row = 1)
            last_index += 1

    # 最終行の次の行から書き込み
    gd.set_with_dataframe(worksheet, df, row = last_index + 1, include_column_header = False)
'''