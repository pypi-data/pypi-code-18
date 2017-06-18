
from ws_sheets_server.tests.conf.simple import Conf as Conf1

class Conf(Conf1):
    @classmethod
    def prepare(cls, mode):
        Conf1.prepare(mode)

        cls.log_console()



