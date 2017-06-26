#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process
from api.api_server import start_api_server
from handler.agent_task import handle_task
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # start_api_server()
    # handle_task(get_queue())
    p1 = Process(target=start_api_server)
    p2 = Process(target=handle_task)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
