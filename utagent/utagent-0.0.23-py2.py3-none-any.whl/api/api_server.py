#!/usr/bin/env python
# -*- coding: utf-8 -*-

import slave.config as config
from bottle import Bottle, run, request
import slave.api.httpizza as api
import slave.util.sys_info as sysInfo
from slave.util.adb import AdbTools
from slave.globalvar import get_queue
import json
import logging
import sys

logger = logging.getLogger(__name__)

app = Bottle()
a = AdbTools()


def start_api_server():
    run(app, host='', port=config.API_PORT)
    api.post_agent(sysInfo.get_host_ip(), config.API_PORT, sysInfo.get_host_name())
    try:
        brand = a.get_device_brand()
        model = a.get_device_model()
        os_version = a.get_device_sdk_version()
        rom_version = a.get_device_android_version()
        device_id = a.get_device_id()
        api.post_device(sysInfo.get_host_ip(), brand, model, os_version,
                        rom_version, device_id)
    except KeyboardInterrupt:
        logger.info("no devices/emulators found")
        sys.exit()


@app.post('/task')
def task():
    get_queue().put(request.body)


@app.get('/ping')
def ping():
    return json.dumps(True)
