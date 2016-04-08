# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2015 hualahuala.com, All Rights Reserved
#
################################################################################
import logging
import logging.handlers as handlers
import time
from comm_decorator import singleton
import client_conf

@singleton
class TkLog(object):
    """docstring for ClassName"""
    def __init__(self):
        self.logger = None
        self.init_log(client_conf.NAME,client_conf.LEVEL,client_conf.HOST,client_conf.PORT,client_conf.CAPACITY)
    def init_log(self, name, level, host, port, capacity = 100):
        target = handlers.SocketHandler(host, port)
        if capacity > 0:
            hdlr = handlers.MemoryHandler(capacity, logging.ERROR, target)
        else:
            hdlr = target
        hdlr.setLevel(level)
        self.logger = logging.getLogger(name)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(level)

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
