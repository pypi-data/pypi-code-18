# -*- coding: utf-8 -*-
import configparser
import os

from .definitions import CONFIG_PATH


class BadConfigError(Exception):
    pass


def get_config():
    """
    Return parsed config.ini files.
    """
    config = configparser.ConfigParser()

    # Check if the path is to a valid file
    if not os.path.isfile(CONFIG_PATH):
        raise BadConfigError('{} not found'.format(CONFIG_PATH))

    # Read config
    with open(CONFIG_PATH) as f:
        config.read_file(f)

    # Override with user ini files.
    config.read(['/etc/googlespider/config.ini', os.path.expanduser('~/.googlespider.ini'), 'config.ini'])

    return config
