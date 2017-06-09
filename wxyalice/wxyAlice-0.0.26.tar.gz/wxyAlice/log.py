import logging


fmt = '%(asctime)s %(filename)s[line:%(lineno)03d] %(levelname)s %(message)s'

class Log(object):
    def __init__(self, fmt=fmt,lvl=logging.DEBUG):
        self.fmt = fmt
        self.lvl = lvl
        logging.basicConfig(level=self.lvl, format=self.fmt)

    def Info(self, msg):
        logging.info(msg)


