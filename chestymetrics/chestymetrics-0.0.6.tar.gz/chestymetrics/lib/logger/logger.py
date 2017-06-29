import logging
from systemd import  journal

log = logging.getLogger('demo')

class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger('chestymetrics')
        self.logger.addHandler(journal.JournaldLogHandler())
        self.logger.setLevel(logging.INFO)

    def info(self, msg):
        self.logger.info(msg=msg)

    def warn(self, msg):
        self.logger.warning(msg=msg)

    def error(self, msg):
        self.logger.error(msg=msg)
