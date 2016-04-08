#encoding=utf-8
import logging
import logging.handlers
import sys
from comm_decorator import singleton

@singleton
class TkLog(object):
    def __init__(self, log_module = "rm_server", log_filename = "rm.log", log_level = logging.DEBUG, print_screen = True):
        self.logger = logging.getLogger(log_module)
        formatter = logging.Formatter('%(asctime)s - %(process)d - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.handlers.TimedRotatingFileHandler(log_filename, 'H', 1, 10)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.print_screen = print_screen
        if self.print_screen:
            stream_logger = logging.StreamHandler(sys.stderr)
            self.logger.addHandler(stream_logger)
        self.log_level = log_level
        self.logger.setLevel(self.log_level)

    def set_file_name(self, name):
        formatter = logging.Formatter('%(asctime)s - %(process)d - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.handlers.TimedRotatingFileHandler(name, 'H', 1, 10)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        if self.print_screen:
            stream_logger = logging.StreamHandler(sys.stderr)
            self.logger.addHandler(stream_logger)
        self.logger.setLevel(self.log_level)

    def debug(self, data):
        self.logger.debug(data)

    def info(self, data):
        self.logger.info(data)

    def warn(self, data):
        self.logger.warning(data)

    def error(self, data):
        self.logger.error(data)

    def critical(self, data):
        self.logger.critical(data)

    def set_log_level(self, level):
        self.log_level = level
        self.logger.setLevel(self.log_level)
