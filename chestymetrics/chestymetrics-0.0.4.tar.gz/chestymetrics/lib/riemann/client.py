from riemann_client.transport import TCPTransport
from riemann_client.client import QueuedClient

from ..rabbitmq.message import Message
from ..consumer.consumer import ConsumerClient


class RiemannClient(ConsumerClient):
    def __init__(self, config):
        self.client = QueuedClient(TCPTransport(config.riemann_host, config.riemann_port))
        self.client.transport.connect()

    def recieve_message(self, message):
        for hostname, metrics in message.items():
            for metric in metrics:
                message = Message(**metric)
                self.client.event(service=message.service, metric_f=message.metric, host=hostname)

            self.client.flush()
