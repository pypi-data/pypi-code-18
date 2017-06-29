import json

import click
import socket

import time

from .lib.collector.memory import MemoryMetricsCollector
from .lib.collector.disk import DiskMetricsCollector
from .lib.collector.network import NetworkMetricsCollector
from .lib.riemann.client import RiemannClient
from .lib.cassandra.client import CassandraClient
from .lib.consumer.consumer import Consumer
from .lib.collector.cpu import CPUMetricsCollector
from .lib.collector.collector import MetricsCollector
from .lib.logger.logger import Logger
from .lib.config.config import Config
from .lib.rabbitmq.client import RabbitMQConsumer, RabbitMQPublisher


@click.group()
def cli():
    pass


@cli.command()
@click.option('--rabbitmq-host', default='192.168.1.2', type=click.types.STRING)
@click.option('--rabbitmq-port', default=5672, type=click.types.INT)
@click.option('--rabbitmq-queue', default='chestymetrics', type=click.types.STRING)
@click.option('--rabbitmq-exchange', default='', type=click.types.STRING)
@click.option('--interval', default=60.0)
def reporter(**kwargs):
    config = Config(**kwargs)
    logger = Logger()
    logger.info('Starting chestymetrics...')
    logger.info('connecting to RabbitMQ...')
    with RabbitMQPublisher(config) as rabbitmq_client:
        logger.info('connected.')
        hostname = socket.gethostname()
        metrics_collector = MetricsCollector()
        metrics_collector.register(CPUMetricsCollector())
        metrics_collector.register(NetworkMetricsCollector())
        metrics_collector.register(DiskMetricsCollector())
        metrics_collector.register(MemoryMetricsCollector())

        starttime=time.time()
        while True:
            rabbitmq_client.push_message(
                json.dumps({hostname: [message.to_dict() for message in metrics_collector.collect_metrics()]})
            )
            time.sleep(kwargs.get('interval') - ((time.time() - starttime) % kwargs.get('interval')))


@cli.command()
@click.option('--rabbitmq-host', default='192.168.1.2', type=click.types.STRING)
@click.option('--rabbitmq-port', default=5672, type=click.types.INT)
@click.option('--rabbitmq-queue', default='chestymetrics', type=click.types.STRING)
@click.option('--rabbitmq-exchange', default='', type=click.types.STRING)
@click.option('--cassandra-endpoints', default='192.168.1.51,192.168.1.52,192.168.1.53', type=click.types.STRING)
@click.option('--riemann-host', default='192.168.1.2', type=click.types.STRING)
@click.option('--riemann-port', default=5555, type=click.types.INT)
def consumer(**kwargs):
    config = Config(**kwargs)
    logger = Logger()
    logger.info('starting chestymetrics consumer...')
    logger.info('connecting to RabbitMQ...')
    consumer = Consumer()
    with RabbitMQConsumer(config) as rabbitmq_client:
        with CassandraClient(config) as cassandra_client:
            consumer.register(cassandra_client)
            consumer.register(RiemannClient(config))
            logger.info('connected')
            rabbitmq_client.consume(consumer.callback)

if __name__ == '__main__':
    cli()
