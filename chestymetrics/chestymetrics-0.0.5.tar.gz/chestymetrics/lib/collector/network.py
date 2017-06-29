import datetime

import psutil

from ..rabbitmq.message import Message
from ..collector.collector import BaseCollector


class NetworkMetricsCollector(BaseCollector):
    def __init__(self):
        self.last_counters = {}
        self.last_collect_time = datetime.datetime.now()

    def collect_metrics(self):
        network_stats = psutil.net_io_counters()._asdict()
        collect_time = datetime.datetime.now()
        collect_interval = (collect_time - self.last_collect_time).seconds
        self.last_collect_time = collect_time
        collect_interval = 1 if collect_interval < 1 else collect_interval

        messages = [
            Message('net/' + k + '/sec', (v - self.last_counters.get(k, 0)) / collect_interval)
            for k, v in network_stats.items()
        ]

        self.last_counters = network_stats
        return messages
