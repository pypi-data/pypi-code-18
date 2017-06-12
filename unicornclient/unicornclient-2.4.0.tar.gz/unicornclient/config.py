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
