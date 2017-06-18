import os
import modconf
import ssl

from ws_web_aiohttp.tests.conf.log import *
from ws_web_aiohttp.tests.conf.web_secure import *

#CONF_DIR = os.path.join(os.environ['HOME'], 'config')
CONF_DIR = '/etc/ws_web_aiohttp/conf/'

google_oauth2 = modconf.import_conf('google_oauth2', CONF_DIR)

PG = modconf.import_conf('postgresql', CONF_DIR)

ws_sheets_server = modconf.import_conf('ws_sheets_server.tests.conf.simple')



