#encoding=utf-8
import logging
import logging.handlers as handlers
import time

def get_logger(name, level, host, port, capacity = 1024):
    target = handlers.SocketHandler(host, port)
    if capacity > 0:
        hdlr = handlers.MemoryHandler(capacity, logging.ERROR, target)
    else:
        hdlr = target
    hdlr.setLevel(level)
    logger = logging.getLogger(name)
    logger.addHandler(hdlr)
    logger.setLevel(level)
    return logger

def get_cgi_logger(level, host, port, capacity = 1024):
    return get_logger('cgi_server', level, host, port, capacity)

def get_bind_server_logger(level, host, port, capacity = 1024):
    return get_logger('bind_thirdparty', level, host, port, capacity)

def get_message_server_logger(level, host, port, capacity = 1024):
    return get_logger('message_server', level, host, port, capacity)

def get_bank_server_logger(level, host, port, capacity = 1024):
    return get_logger('bank_server', level, host, port, capacity)

def get_risk_server_logger(level, host, port, capacity = 1024):
    return get_logger('risk_server', level, host, port, capacity)

def get_crawl_logger(level, host, port, capacity = 1024):
    return get_logger('crawl_thirdparty_server', level, host, port, capacity)

#@singleton
#class TkLogger(object):
#    def __init__(self, log_module, host, port, log_level = logging.DEBUG):
#        self.logger = get_logger(log_module, log_level, host, port)

def test():
    logger = get_logger('test', logging.DEBUG, '127.0.0.1', 9095)
    for i in range(10):
        logger.debug('test')
        #logger.error('error test')
        time.sleep(1)

if __name__ == '__main__':
    test()