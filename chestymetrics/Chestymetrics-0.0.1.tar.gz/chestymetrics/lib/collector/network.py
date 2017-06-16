import datetime

import psutil

from ..rabbitmq.message import Message
from ..collector.collector import BaseCollector


class NetworkMetricsCollector(BaseCollector):
    def __init__(self):
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0
        self.last_packets_sent = 0
        self.last_packets_recv = 0
        self.last_errin = 0
        self.last_errout = 0
        self.last_dropin = 0
        self.last_dropout = 0
        self.last_collect_time = datetime.datetime.now()

    def collect_metrics(self):
        network_stats = psutil.net_io_counters()
        collect_time = datetime.datetime.now()
        collect_interval = (collect_time - self.last_collect_time).seconds
        self.last_collect_time = collect_time
        collect_interval = 1 if collect_interval < 1 else collect_interval
        messages = [
            Message('net/bytes_sent/sec', (network_stats.bytes_sent - self.last_bytes_sent) / collect_interval),
            Message('net/bytes_recv/sec', (network_stats.bytes_recv - self.last_bytes_recv) / collect_interval),
            Message('net/packets_sent/sec', (network_stats.packets_sent - self.last_packets_sent) / collect_interval),
            Message('net/packets_recv/sec', (network_stats.packets_recv - self.last_packets_recv) / collect_interval),
            Message('net/errin/sec', (network_stats.errin - self.last_errin) / collect_interval),
            Message('net/errout/sec', (network_stats.errout - self.last_errout) / collect_interval),
            Message('net/dropin/sec', (network_stats.dropin - self.last_dropin) / collect_interval),
            Message('net/dropout/sec', (network_stats.dropout - self.last_dropout) / collect_interval)
        ]
        self.last_bytes_sent = network_stats.bytes_sent
        self.last_bytes_recv = network_stats.bytes_recv
        self.last_packets_sent = network_stats.packets_sent
        self.last_packets_recv = network_stats.packets_recv
        self.last_errin = network_stats.errin
        self.last_errout = network_stats.errout
        self.last_dropin = network_stats.dropin
        self.last_dropout = network_stats.dropout

        return messages
