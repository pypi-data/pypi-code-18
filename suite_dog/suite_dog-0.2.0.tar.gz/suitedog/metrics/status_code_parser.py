#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Author: Rajat Gupta
Description: Module to parse status code of the logs and send to datadog server
"""

import time
from datetime import datetime
from settings import status_code_metric_name as metric_name


def parse_status_code(logger, line):
    """
    Parse the status code from the app logs to JSON
    """

    try:
        log_message_index = line.find('{"')
        log = line[log_message_index:]

        final_log = log.replace("{", "").replace("}", "")

        elements = final_log.split(",")
        log_message = {}

        for element in elements:
            element = element.strip('"').strip("'")
            key, value = element.split('":')

            log_message[key] = value.strip('"').strip("'")

        date = log_message["@timestamp"]
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        date = time.mktime(date.timetuple())
        metric_value = float(log_message['status'])

        del log_message['@timestamp']

        return (metric_name, date, metric_value, log_message)
    except:
        pass
