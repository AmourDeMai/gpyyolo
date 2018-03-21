# encoding=utf-8

import logging
import logging.handlers
import os


class Log:
    logger = None  # singleton for logger

    levels = {'n': logging.NOTSET,
              'd': logging.DEBUG,
              'i': logging.INFO,
              'w': logging.WARN,
              'e': logging.ERROR,
              'c': logging.CRITICAL}

    log_file = 'log' + os.sep + 'gpyyolo.log'
    log_format = '%(levelname)s| %(asctime)s| gpyyolo %(process)s| %(proce'\
                 'ssName)s| %(filename)s| [line:%(lineno)d]| %(message)s'
    log_max_byte = 20 * 1024 * 1024
    log_backup_num = 10

    @staticmethod
    def get_log_folder():
        filepath = os.path.dirname(__file__)  # detect this file's address
        if filepath is None:
            return None

        return filepath.split('util')[0]

    @staticmethod
    def get_logger(log_level='i'):  # define a singleton

        if Log.logger is not None:
            return Log.logger

        Log.logger = logging.getLogger()
        log_file_path = Log.get_log_folder()
        if not log_file_path:
            log_file_path = '..' + os.sep + Log.log_file
        else:
            log_file_path += Log.log_file

        Log.logger.info("the path for log is %s", log_file_path)
        # output log into log file
        log_handler = logging.handlers.RotatingFileHandler(
            filename=log_file_path,
            maxBytes=Log.log_max_byte,
            backupCount=Log.log_backup_num)
        log_fmt = logging.Formatter(Log.log_format)
        log_handler.setFormatter(log_fmt)
        Log.logger.addHandler(log_handler)

        # output log onto console
        console = logging.StreamHandler()
        console.setLevel(Log.levels.get(log_level))
        console.setFormatter(log_fmt)
        # TODO: console is logged to supervised log
        Log.logger.addHandler(console)

        Log.logger.setLevel(Log.levels.get(log_level))

        return Log.logger


if __name__ == '__main__':
    log1 = Log.get_logger()
    log1.debug("this is a debug msg!")
    log1.fatal("this is a debug msg!")
    log1.warn("this is a warn msg!")
    log1.critical("this is a critical msg!")
