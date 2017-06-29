import psutil

from ..collector.collector import BaseCollector
from ..rabbitmq.message import Message


class CPUMetricsCollector(BaseCollector):
    def collect_metrics(self):
        return [
            Message('cpu/times_' + k, v)
            for k, v in psutil.cpu_times()._asdict().items()
        ] + [Message(service='cpu/percent', metric=psutil.cpu_percent())]
