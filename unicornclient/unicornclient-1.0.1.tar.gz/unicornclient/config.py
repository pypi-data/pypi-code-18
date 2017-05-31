import os

HOST = 'localhost'
PORT = 8080

ENV = os.getenv('PYTHONENV', 'dev')

if ENV == 'prod':
    HOST = 'unicorn.ahst.fr'

DEFAULT_ROUTINES = ['ping', 'status', 'system']

CUSTOM_ROUTINES = {
    '00000000dd275177': ['travis'],
    '000000008a09c09c': ['sun'],
    '0000000063ceb3e8': ['dothat'],
}
