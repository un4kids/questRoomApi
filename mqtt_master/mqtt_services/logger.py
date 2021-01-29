import os
import logging
from logging.handlers import RotatingFileHandler

def reg_logger():
    # create logger
    logger = logging.getLogger("master_log")
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create handler to write error logs in file
    os.makedirs(os.path.dirname('./logs/mqtt_master.log'), exist_ok=True)
    log_reg = RotatingFileHandler('./logs/mqtt_master.log', mode='a', maxBytes=5*1024*1024,
                        backupCount=2, encoding=None, delay=0)
    log_reg.setLevel(logging.DEBUG)

    # create formatter for logger output
    formatter = logging.Formatter('\n[%(levelname)s] - %(asctime)s - %(name)s - %(message)s')

    # add formatter to handlers
    ch.setFormatter(formatter)
    log_reg.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(ch)
    logger.addHandler(log_reg)
    return logger
