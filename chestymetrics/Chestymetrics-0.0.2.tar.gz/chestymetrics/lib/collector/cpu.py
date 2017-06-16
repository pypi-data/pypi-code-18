import psutil

from ..collector.collector import BaseCollector
from ..rabbitmq.message import Message


class CPUMetricsCollector(BaseCollector):
    def collect_metrics(self):
        cpu_times = psutil.cpu_times()
        return [
            Message(service='cpu/percent', metric=psutil.cpu_percent()),
            Message(service='cpu/times_user', metric=cpu_times.user),
            Message(service='cpu/times_nice', metric=cpu_times.nice),
            Message(service='cpu/times_system', metric=cpu_times.system),
            Message(service='cpu/times_idle', metric=cpu_times.idle),
            Message(service='cpu/times_iowait', metric=cpu_times.iowait),
            Message(service='cpu/times_irq', metric=cpu_times.irq),
            Message(service='cpu/times_softirq', metric=cpu_times.softirq),
            Message(service='cpu/times_steal', metric=cpu_times.steal),
            Message(service='cpu/times_guest', metric=cpu_times.guest),
            Message(service='cpu/times_guest_nice', metric=cpu_times.guest_nice)
            ]
