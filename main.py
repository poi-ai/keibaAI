import log
import os
import sys

def main():
    '''主処理'''

    # 設定ファイルの読み込み
    try:
        import settings
    except ModuleNotFoundError as e:
        logger.error('settings.pyが見つかりません。リポジトリのルートディレクトリ直下にsettings.pyを配置してください')
        return

    # 共通用ディレクトリをモジュールパスに追加
    # README.mdの「共通用ディレクトリをモジュールパスに追加する」を実行していた場合はなくてもよい
    sys.path.append(os.path.join('src', 'common'))

    # パラメータのバリデートチェック/起動させるシステムの選択
    # データ取得かデータ分析か
    if settings.SCRIPT_TYPE == 'scraping':
        # 取得するデータの種類
        if settings.DATA_TYPE == 'odds':
            # 取得する期間
            if settings.DATA_TIME == 'past':
                pass
            elif settings.DATA_TIME == 'now':
                pass
            else:
                validate_error('DATA_TIME')
        elif settings.DATA_TYPE == 'race':
            # 取得する期間
            if settings.DATA_TIME == 'past':
                pass
            elif settings.DATA_TIME == 'now':
                pass
            else:
                validate_error('DATA_TIME')
        else:
            validate_error('DATA_TYPE')
    elif settings.SCRIPT_TYPE == 'analysis':
        validate_error('SCRIPT_TYPE', 'analysis')
    else:
        validate_error('SCRIPT_TYPE')


def validate_error(variable, unavailable = None):
    '''設定ファイルのパラメータに誤りがあった場合'''
    if unavailable == None:
        logger.error(f'settings.pyの{variable}の値が正しくありません。再度パラメータを確認してください')
    else:
        logger.error(f'settings.pyの{variable}に{unavailable}は現在設定できません。別の値を設定してください')
    exit()

if __name__ == '__main__':
    logger = log.Logger()
    main()