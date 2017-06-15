
from ws_sheets_server.tests.conf.simple import *

LOGGING['loggers']['__main__']['handlers'] = ['console']
LOGGING['loggers']['ws_sheets']['handlers'] = ['console']
LOGGING['loggers']['ws_sheets_server']['handlers'] = ['console']

