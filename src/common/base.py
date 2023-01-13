import line
import log

class Base:
    '''共通処理のloggerインスタンス生成とエラー通知メソッドを記載'''
    def __init__(self):
        self.logger = log.Logger()

    def error_output(self, message, e, stacktrace):
        '''エラー時のログ出力/LINE通知を行う

        Args:
            message(str) : エラーメッセージ
            e(str) : エラー名
            stacktrace(str) : スタックトレース
        '''
        self.logger.error(message)
        self.logger.error(e)
        self.logger.error(stacktrace)
        line.send(f'{message}\n{e}\n{stacktrace}')