from ..rabbitmq.message import Message


class MetricsCollector(object):
    def __init__(self):
        self.collectors = []

    def register(self, collector):
        self.collectors.append(collector)

    def collect_metrics(self):
        return [message for collector in self.collectors for message in collector.collect_metrics()]


class BaseCollector(object):
    def collect_metrics(self) -> list:
        raise NotImplementedError()
