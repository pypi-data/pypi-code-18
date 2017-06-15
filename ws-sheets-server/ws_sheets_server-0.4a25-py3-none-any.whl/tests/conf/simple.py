import os
import modconf

conf_sheets = modconf.import_conf('ws_sheets.tests.conf.simple')

LOG_FILE = 'dev/log/ws_sheets_server/debug.log'
LOG_FILE_CELL = 'dev/log/ws_sheets_server/cell/debug.log'

try:
    os.makedirs(os.path.dirname(LOG_FILE))
except os.error: pass

try:
    os.makedirs(os.path.dirname(LOG_FILE_CELL))
except os.error: pass

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename':LOG_FILE,
                'formatter':'basic'
                },
            'file_cell': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename':LOG_FILE_CELL,
                'formatter':'basic'
                },
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'basic'
                },
            },
        'loggers':{
            '__main__': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                },
            'ws_sheets': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                },
            'ws_sheets_server': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                },
            'ws_sheets.cell/cell': {
                'handlers': ['file_cell'],
                'level': 'DEBUG',
                'propagate': True,
                },
            },
        'formatters': {
            "basic":{
                "format":"%(asctime)s %(process)s %(module)10s %(levelname)s %(message)s"
                }
            }
        }

PORT = 10003

STORAGE_FOLDER = 'dev/storage'

try:
    os.makedirs(STORAGE_FOLDER)
except os.error: pass







