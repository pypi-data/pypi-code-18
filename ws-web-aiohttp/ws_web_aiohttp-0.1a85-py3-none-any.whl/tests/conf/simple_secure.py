import os
import modconf
import ssl

from ws_web_aiohttp.tests.conf.web_secure import Conf as Conf_web

class Conf(Conf_web):
    @classmethod
    def prepare(cls, mode):
        Conf_web.prepare(mode)

        #cls.CONF_DIR = os.path.join(os.environ['HOME'], 'config')
        cls.CONF_DIR = '/etc/ws_web_aiohttp/conf/'

        cls.google_oauth2 = modconf.import_conf('google_oauth2', cls.CONF_DIR)

        cls.PG = modconf.import_conf('postgresql', cls.CONF_DIR)

        cls.ws_sheets_server = modconf.import_class('ws_sheets_server.tests.conf.simple', 'Conf', (mode,))


