import inspect
import line
import log
from pathlib import Path

class Base:
    '''共通処理のloggerインスタンス生成とエラー通知メソッドを記載'''

    def __init__(self, logger_filename = None):
        if logger_filename != None:
            self.logger = log.Log(logger_filename)
        else:
            self.logger = log.Log(Path(inspect.stack()[1].filename).stem)

    def error_output(self, message, e = None, stacktrace = None, line_flg = True):
        '''
        エラー時のログ出力/LINE通知を行う

        Args:
            message(str) : エラーメッセージ
            e(str) : エラー名
            stacktrace(str) : スタックトレース(traceback.format_exc())
        '''
        line_message = message
        self.logger.error(message)

        if e != None:
            self.logger.error(e)
            line_message += f'\n{e}'

        if stacktrace != None:
            self.logger.error(stacktrace)
            line_message += f'\n{stacktrace}'

        if line_flg:
            line.send(line_message)

    def validate_error(self, column_name, message):
        '''
        バリデーションチェックに引っかかったときのログ出力を行う

        Args:
            columns_name(srt): カラム名
            message(str) : エラーメッセージ

        '''
        classname = inspect.currentframe().f_back.f_locals.get('__qualname__')
        self.logger.error(f'{classname}クラスの{column_name}でエラー {message}')
