import datetime

import psutil

from ..rabbitmq.message import Message
from ..collector.collector import BaseCollector


class DiskMetricsCollector(BaseCollector):
    def __init__(self):
        self.partitions = psutil.disk_partitions()
        self.last_io_counters = None
        self.last_collect_time = datetime.datetime.now()

    def collect_metrics(self):
        messages = []
        io_counters = psutil.disk_io_counters()._asdict()
        collect_time = datetime.datetime.now()
        collect_interval = (collect_time - self.last_collect_time).seconds
        self.last_collect_time = collect_time
        for part in self.partitions:
            disk_usage = psutil.disk_usage(part.device)
            messages.extend(
                [
                    Message(part.mountpoint + '/total_bytes', disk_usage.total),
                    Message(part.mountpoint + '/used_bytes', disk_usage.used),
                    Message(part.mountpoint + '/free_bytes', disk_usage.free),
                    Message(part.mountpoint + '/percent_used', disk_usage.percent)
                ]
            )
        if self.last_io_counters is not None:
            messages.extend(
                [
                    Message('disk/' + k + '/sec', (v - self.last_io_counters[k]) / collect_interval)
                    for k, v in psutil.disk_io_counters()._asdict().items()
                ]
            )
        self.last_io_counters = io_counters
        return messages
