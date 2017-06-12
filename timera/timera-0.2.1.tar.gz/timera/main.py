# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import logging

try:
    # noinspection PyCompatibility
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences
    from configparser import ConfigParser

from . import collector
from . import db
from . import util
from .exc import TimeraInvalidArgs

log = logging.getLogger()


def setup_log(debug):
    log_level = logging.DEBUG if debug else logging.INFO
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(threadName)-9s %(message)s')
    sh.setFormatter(formatter)
    log.addHandler(sh)
    log.setLevel(log_level)


def setup_env():
    util.delete_proxy_env()


def reset_db(config, confirm=True):
    idbc = db.get_client(config)
    db.reset(idbc, config, confirm=confirm)


def parse_config(fname):
    # make sure we can read fname so we get an error now, since ConfigParser.read() doesn't
    with open(fname, 'r') as f:
        f.read()
    here = os.path.dirname(os.path.abspath(fname))
    defaults = dict(here=here)
    config = ConfigParser(defaults)
    config.read(fname)
    return config


def print_usage(args):
    cmd = os.path.basename(args[0])
    print('usage: %s <config_filename> (start | reset_db)' % cmd)
    print('example: %s config.ini start' % cmd)


def get_args(args):
    actions = ['start', 'reset_db']
    if len(args) != 3 or args[2] not in actions:
        print_usage(args)
        raise TimeraInvalidArgs('invalid arguments: %r' % args)
    return args


def main(args=sys.argv):
    """:return: int for sys.exit()"""
    try:
        cmd, config_fname, action = get_args(args)
    except TimeraInvalidArgs:
        return 1
    config = parse_config(config_fname)
    if action == 'reset_db':
        reset_db(config)
        return 0
    debug = util.asbool(config.get('main', 'debug'))
    setup_log(debug)
    setup_env()
    collector.run_loop(config)
    return 0
