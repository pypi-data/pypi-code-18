import psutil

from ..collector.collector import BaseCollector
from ..rabbitmq.message import Message


class MemoryMetricsCollector(BaseCollector):
    def collect_metrics(self):
        return [
            Message('memory/' + k, v)
            for k, v in psutil.virtual_memory()._asdict().items()
        ]
