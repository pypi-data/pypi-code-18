import logging

from eva.conf import settings
from importlib import import_module


def load_models():
    m = import_module(settings.MODELS_MODULE)
    if m:
        logging.debug('load models SUCCESS')


def create_table():
    logging.error('uncompleted!')


def drop_table():
    logging.error('uncompleted!')
