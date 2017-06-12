import os
import logging

ENV = os.getenv('PYTHONENV', 'prod')

LOG_LEVEL = logging.DEBUG
if ENV == 'prod':
    LOG_LEVEL = logging.INFO

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=LOG_LEVEL)

HOST = 'localhost'
PORT = 8080

if ENV == 'prod':
    HOST = 'unicorn.ahst.fr'

DEFAULT_ROUTINES = ['auth', 'ping', 'status', 'system']

CUSTOM_ROUTINES = {
    '00000000dd275177': ['travis'], # unicorn phat
    '0000000063ceb3e8': ['dothat'], # microdot phat
    '000000008a09c09c': [],         # unicorn hat
    '00000000defe475f': [],         # octocam
}
