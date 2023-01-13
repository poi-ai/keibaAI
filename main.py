import log
import os
import sys

def main():
    '''主処理'''

    # 設定ファイルの読み込み
    try:
        import config
    except ModuleNotFoundError as e:
        logger.error('config.pyが見つかりません。リポジトリのルートディレクトリ直下にconfig.pyを配置してください')
        return

    # 共通用ディレクトリと設定用ディレクトリモジュールパスに追加
    # README.mdの「共通用ディレクトリをモジュールパスに追加する」を実行していた場合はなくてもよい
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'common'))
    sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

    # パラメータのバリデートチェック/起動させるシステムの選択
    # データ取得かデータ分析か
    if config.SCRIPT_TYPE == 'scraping':
        # 取得するデータの種類
        if config.DATA_TYPE == 'odds':
            # 取得する期間
            if config.DATA_TIME == 'past':
                pass
            elif config.DATA_TIME == 'now':
                pass
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
            from src.scraping.jbis import horse
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

if __name__ == '__main__':
    logger = log.Logger()
    main()