#!/usr/bin/env python3
import functools
import logging
import os
import sys
import shutil
import jinja2

import aiohttp
import aiohttp.web
import aiohttp_security
import aiohttp_session.redis_storage
import aioredis
import aiopg
import aiopg.sa
import sys
import json
import requests_oauthlib
import ssl
import modconf
import argparse
import asyncio
import pickle

import ws_sheets.tests.functions
import ws_sheets_server

import ws_web_aiohttp.server

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)

def runserver(args):
    ws_web_aiohttp.server.runserver(args)

def install(args):
    # copy systemd file
    shutil.copyfile(
            os.path.join(BASE_DIR, 'ws_web_aiohttp.service'),
            os.path.join('/lib/systemd/system', 'ws_web_aiohttp.service'))

    config_file_dst = os.path.join('/etc/ws_web_aiohttp/conf', 'simple.py')

    # make etc directory
    try:
        os.makedirs(os.path.dirname(config_file_dst))
    except: pass
    
    # copy default config file
    shutil.copyfile(
            os.path.join(BASE_DIR, 'tests/conf/simple.py'),
            config_file_dst)

def main(argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    parser_runserver = subparsers.add_parser('runserver')
    parser_runserver.add_argument('--conf_dir',
            nargs=1,
            default=(None,))
    parser_runserver.add_argument('conf_mod')
    parser_runserver.set_defaults(func=runserver)

    parser_install = subparsers.add_parser('install')
    parser_install.set_defaults(func=install)

    args = parser.parse_args(argv[1:])
    args.func(args)

if __name__=='__main__':
    main(sys.argv)

