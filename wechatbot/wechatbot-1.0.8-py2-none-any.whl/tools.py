# -*- coding:utf-8 -*-
import time
import sys
import logging

from wechatbot.consts import (
    MSG,
    RED,
    GREEN,
    NC
)

now = lambda : time.time()

red_alert = lambda content: MSG.format(color=RED, content=content, nc=NC)
green_alert = lambda content: MSG.format(color=GREEN, content=content, nc=NC)


def create_logger(app_name):
    """Creates a logger for the given application.
    """
    _logger = logging.getLogger(app_name)
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    file_handler = logging.FileHandler("{}.log".format(app_name))
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    _logger.setLevel(logging.INFO)
    # print log to file and console
    _logger.addHandler(stream_handler)
    _logger.addHandler(file_handler)
    return _logger

if __name__ == '__main__':
    pass
