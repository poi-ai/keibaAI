import log
import os
import sys
import config

def main():
    '''主処理'''

    # 設定ファイルの読み込み TODO ここに置くとargs_check()で読めない
    #try:
    #    import config
    #except ModuleNotFoundError as e:
    #    logger.error('config.pyが見つかりません。リポジトリのルートディレクトリ直下にconfig.pyを配置してください')
    #    return

    # 共通用ディレクトリと設定用ディレクトリモジュールパスに追加
    # README.mdの「共通用ディレクトリをモジュールパスに追加する」を実行していた場合はなくてもよい
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'common'))
    sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

    # コマンドライン引数がある場合そちらの設定値を優先する(cron用)
    try:
        args_check()
    except Exception as e:
        logger.error('コマンドライン引数チェック処理でエラー')

    # パラメータのバリデートチェック/起動させるシステムの選択
    # データ取得かデータ分析か
    if config.SCRIPT_TYPE == 'scraping':
        # 取得するデータの種類
        if config.DATA_TYPE == 'odds':
            # 取得する期間
            if config.DATA_TIME == 'past':
                pass
            elif config.DATA_TIME == 'now':
                from src.scraping.nowodds import NowOdds
                odds = NowOdds()
                odds.main()
            else:
                validate_error('DATA_TIME')
        elif config.DATA_TYPE == 'race':
            # 取得する期間
            if config.DATA_TIME == 'past':
                pass
            elif config.DATA_TIME == 'now':
                pass
            else:
                validate_error('DATA_TIME')
        elif config.DATA_TYPE == 'horse':
            # フォルダ読み込み
            from src.scraping.access.jbis import horse
            # インスタンス生成
            h = horse.Horse(config.JBIS_HORSE_ID)
            # 失敗したら終了
            if not h:
                return
            # 主処理
            h.main()
        else:
            validate_error('DATA_TYPE')
    elif config.SCRIPT_TYPE == 'analysis':
        validate_error('SCRIPT_TYPE', 'analysis')
    else:
        validate_error('SCRIPT_TYPE')


def validate_error(variable, unavailable = None):
    '''設定ファイルのパラメータに誤りがあった場合'''
    if unavailable == None:
        logger.error(f'config.pyの{variable}の値が正しくありません。再度パラメータを確認してください')
    else:
        logger.error(f'config.pyの{variable}に{unavailable}は現在設定できません。別の値を設定してください')
    exit()

def args_check():
    '''引数から起動させるシステムの選択(cron用)
       プロセス起動中のみ一時的に設定値を書き換える
       現在起動できるのは単複リアルタイムオッズ取得のみ

    Args:
       第二引数 : 起動システム
                  1 → 単複リアルタイムオッズ取得
       第三引数 : 主催
                  1 → JRA & NAR
                  2 → JRAのみ
                  3 → NARのみ
       第四引数 : CSV出力するか ( 1 or 0 )
       第五引数 : DB出力するか ( 1 or 0)

    '''
    args, ln = sys.argv, len(sys.argv)

    # 引数なしの場合
    if ln < 2: return

    # 起動システム設定
    if str(args[2]) == '1':
        config.SCRIPT_TYPE = 'scraping'
        config.DATA_TYPE = 'odds'
        config.DATA_TIME = 'now'

    if ln == 2: return

    # 主催設定
    config.OUTPUT_CSV = '1' if str(args[2]) == '1' else 'JRA' if str(args[2]) == '2' else 'NAR'

    if ln == 3: return

    # CSV出力設定
    config.OUTPUT_CSV = '1' if str(args[2]) == '1' else '0'

    if ln == 4: return

    # DB出力設定
    config.OUTPUT_DB = '1' if str(args[2]) == '1' else '0'

    return

if __name__ == '__main__':
    logger = log.Logger()
    main()