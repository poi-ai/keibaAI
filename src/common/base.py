import inspect
import line
import log
from pathlib import Path

class Base:
    '''共通処理のloggerインスタンス生成とエラー通知メソッドを記載'''

    def __init__(self, logger_filename = None):
        if logger_filename != None:
            self.logger = log.Logger(logger_filename)
        else:
            self.logger = log.Logger(Path(inspect.stack()[1].filename).stem)

    def error_output(self, message, e = None, stacktrace = None, line_flg = True):
        '''エラー時のログ出力/LINE通知を行う

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