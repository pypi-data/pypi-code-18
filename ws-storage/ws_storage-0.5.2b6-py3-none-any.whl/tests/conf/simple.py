import os
import enum

import modconf

class Conf(object):
    class Mode(enum.Enum):
        DEVELOP=1
        DEPLOY=2
        
        @classmethod
        def from_string(cls, s):
            if s == 'DEVELOP':
                return cls.DEVELOP
            elif s == 'DEPLOY':
                return cls.DEPLOY
            else:
                raise Exception()

    @classmethod
    def log_console(cls):
        for l in cls.LOGGING['loggers'].values():
            l['handlers'] = ['console']

    @classmethod
    def prepare(cls, mode_s, conf_dir=None, impl=None):
        mode = Conf.Mode.from_string(mode_s)

        cls.CONF_DIR = conf_dir

        cls.IMPL = impl if impl is not None else 'AS3'

        if mode == cls.Mode.DEVELOP:
            cls.PORT = 10001
            cls.STORAGE_DIR = 'venv/etc/ws_storage/storage'
            cls.LOG_FILE = 'venv/var/log/ws_storage/debug.log'

        elif mode == cls.Mode.DEPLOY:
            cls.PORT = 10002
            cls.STORAGE_DIR = '/etc/ws_storage/storage'
            cls.LOG_FILE = '/var/log/ws_storage/debug.log'

        try:
            os.makedirs(os.path.dirname(cls.LOG_FILE))
        except os.error: pass

        cls.LOGGING = {
                'version': 1,
                'disable_existing_loggers': False,
                'handlers': {
                    'file': {
                        'level': 'DEBUG',
                        'class': 'logging.FileHandler',
                        'filename': cls.LOG_FILE,
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
                    'ws_storage': {
                        'handlers': ['file'],
                        'level': 'DEBUG',
                        'propagate': True,
                        },
                    },
                'formatters': {
                    "basic":{
                        "format":"%(asctime)s %(process)s %(module)10s %(funcName)16s %(levelname)7s %(message)s"
                        }
                    }
                }


        cls.AWS = modconf.import_class('aws', 'Conf', (mode_s,), folder=cls.CONF_DIR)



