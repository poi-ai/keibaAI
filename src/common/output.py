import csv
import os

def text(data, file_name):
    '''テキストファイルにデータを出力する

    Args:
        data(str) : 書き込むデータ
        file_name(str) : 出力するファイル名
    '''

    # リポジトリのルートフォルダを指定
    repos_root = os.path.join(os.path.dirname(__file__), '..', '..')
    data_folder = os.path.join(repos_root, 'data')
    text_folder = os.path.join(data_folder, 'text')
    text_file = os.path.join(text_folder, f'{file_name}.txt')

    # dataフォルダチェック。無ければ作成
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # テキストフォルダチェック。無ければ作成
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)

    # テキストファイルのチェック。なければ新規作成、あれば追記
    f = open(text_file, 'a', encoding = 'UTF-8')
    f.write(str(data) + '\n')
    f.close()

def dict_to_csv(data, file_path):
    '''
    dict型のデータを出力する
    キーをカラム名、値をパラメータとして出力する

    Args:
        data: 出力データ
        file_path: 出力先
    '''
    # データが存在していなければ作成
    write_header = not os.path.exists(file_path)

    # データをCSVファイルに追記する
    with open(file_path, 'a', newline = '', encoding = 'UTF-8') as csvfile:
        fieldnames = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        # ファイルが存在しない場合、ヘッダー行を書き込む
        if write_header:
            writer.writeheader()

        # データ行を書き込む
        writer.writerow(data)