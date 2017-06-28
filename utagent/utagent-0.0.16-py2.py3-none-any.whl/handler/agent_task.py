#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from slave.consts import TaskType
from slave.globalvar import get_queue
from slave.handler.macaca_task import (
    run_macaca_test,
    ui_recorder,
    start_macaca_server
)
import logging

logger = logging.getLogger(__name__)


def post_get(name, data):
    return data[name]


def handle_task():
    while True:
        try:
            data = get_queue().get(timeout=3000)
            if data:
                task = json.load(data)
                type = post_get('type', task)
                if type == TaskType.macaca_test:
                    case_url = post_get('case_url', task)
                    name = post_get('name', task)
                    run_macaca_test(name, case_url)
                elif type == TaskType.ui_recorder:
                    ui_recorder()
                elif type == TaskType.macaca_server:
                    start_macaca_server()
        except Exception as e:
            pass
            # logger.exception(e)
