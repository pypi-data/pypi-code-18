
from ws_web_aiohttp.tests.conf.simple_secure import Conf as Conf_simple_secure

class Conf(Conf_simple_secure):
    @classmethod
    def prepare(cls, mode, port=None):
        Conf_simple_secure.prepare(mode, port)

        cls.log_console()

