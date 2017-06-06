#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from aiohttp import web

from tle_storage_service import TleStorageService, load_cfg, LOG_FORMAT

DIR = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    app = TleStorageService(config=load_cfg(path=os.path.join(DIR, 'config', 'server.yaml')))
    web.run_app(app, port=8080)
