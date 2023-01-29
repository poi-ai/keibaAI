import os

def csv(df, file_name):
    '''CSVファイルにデータを出力する

    Args:
        df(pandas.DataFrame) : 書き込むデータ
        file_name(str) : 出力するファイル名
    '''

    # リポジトリのルートフォルダを指定
    repos_root = os.path.join(os.path.dirname(__file__), '..', '..')
    data_folder = os.path.join(repos_root, 'data')
    csv_folder = os.path.join(data_folder, 'csv')
    csv_file = os.path.join(csv_folder, f'{file_name}.csv')

    # dataフォルダチェック。無ければ作成
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # CSVフォルダチェック。無ければ作成
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # CSVファイルチェック。なければカラム名付きで出力、あれば追記
    if not os.path.exists(csv_file):
        df.to_csv(csv_file, index = None, encoding = 'UTF-8')
    else:
        df.to_csv(csv_file, mode = 'a', header = None, index = None, encoding = 'UTF-8')

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