import logging


class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger('chestymetrics')

    def info(self, msg):
        self.logger.info(msg=msg)

    def warn(self, msg):
        self.logger.warning(msg=msg)

    def error(self, msg):
        self.logger.error(msg=msg)
