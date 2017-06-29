import datetime

import psutil

from ..rabbitmq.message import Message
from ..collector.collector import BaseCollector


class DiskMetricsCollector(BaseCollector):
    def __init__(self):
        self.partitions = psutil.disk_partitions()
        self.last_io_counters = {}
        self.last_collect_time = datetime.datetime.now()

    def collect_metrics(self):
        io_counters = psutil.disk_io_counters()._asdict()
        collect_time = datetime.datetime.now()
        collect_interval = (collect_time - self.last_collect_time).seconds
        self.last_collect_time = collect_time
        messages = [
            Message('disk/' + k + '/sec',
                    (v - self.last_io_counters.get(k, 0)) / 1 if collect_interval == 0 else collect_interval)
            for k, v in io_counters.items()
            ]
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
        self.last_io_counters = io_counters
        return messages
