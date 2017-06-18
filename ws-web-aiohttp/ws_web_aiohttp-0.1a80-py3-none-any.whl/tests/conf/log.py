import os
import modconf
import ssl

if False: # dev mode
    LOG_FILE = 'dev/log/ws_web_aiohttp/debug.log'
else:
    LOG_FILE = '/var/log/ws_web_aiohttp/debug.log'

try:
    os.makedirs(os.path.dirname(LOG_FILE))
except: pass

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
            'ws_sheets_server': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                },
            'ws_web_aiohttp': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                },
            },
        'formatters': {
            "basic":{
                "format":"%(asctime)s %(module)12s %(levelname)s %(message)s"
                }
            }
        }

