
from ws_web_aiohttp.tests.conf.simple_secure import *

for l in LOGGING['loggers'].values():
    l['handlers'] = ['console']


