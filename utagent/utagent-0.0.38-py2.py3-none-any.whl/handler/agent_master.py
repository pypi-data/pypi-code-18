#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging

from slave.globalvar import get_queue
from slave.config import config
from macaca_worker import MacacaWorker

logger = logging.getLogger(__name__)


def post_get(name, data):
    return data[name]


def handle_task():
    while True:
        try:
            data = get_queue().get(timeout=3000)
            if data:
                agent_task = json.load(data)
                worker_type = post_get('worker_type', agent_task)
                worker_data = post_get('worker_data', agent_task)
                if worker_type == 1:
                    MacacaWorker(config["macaca_dir"], worker_data).run()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.exception(e)
