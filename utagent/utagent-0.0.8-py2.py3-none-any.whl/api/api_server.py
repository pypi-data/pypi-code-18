#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qualityplatform.config as config
from bottle import Bottle, run, request
import qualityplatform.api.httpizza as api
import qualityplatform.util.sys_info as sysInfo
from qualityplatform.util.adb import AdbTools
from qualityplatform.globalvar import get_queue

from qualityplatform.handler.macaca_task import start_macaca_server

app = Bottle()
a = AdbTools()


def start_api_server():
    run(app, host='', port=config.API_PORT)
    api.post_agent(sysInfo.get_host_ip(), config.API_PORT, sysInfo.get_host_name())
    api.post_device(sysInfo.get_host_ip(), a.get_device_brand(), a.get_device_model(), a.get_device_sdk_version(),
                    a.get_device_android_version(), a.get_device_id())
    start_macaca_server()


@app.post('/task')
def task():
    get_queue().put(request.body)
