import os
import modconf
import ssl

from ws_web_aiohttp.tests.conf.log import Conf as Conf_log

class Conf(Conf_log):

    SCHEME = 'https'
    SCHEME_WS = 'wss'
    PORT = 8443

    url = 'www.charlesrymal.com'

    certfile = '/etc/letsencrypt/live/www.charlesrymal.com/fullchain.pem'
    keyfile = '/etc/letsencrypt/live/www.charlesrymal.com/privkey.pem'
    
    try:
        SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        SSL_CONTEXT.load_cert_chain(certfile, keyfile)
    except:
        SSL_CONTEXT = None

    STATIC_DIR = '/var/www/ws_web_aiohttp/static'

    @classmethod
    def prepare(cls, mode, port=None):
        Conf_log.prepare(mode)

        if port is not None:
            cls.PORT = port

    @classmethod
    def url_root(cls):
        return '{}://localhost:{}'.format(cls.SCHEME, cls.PORT)

    @classmethod
    def ws_root(cls):
        return '{}://localhost:{}'.format(cls.SCHEME_WS, cls.PORT)


