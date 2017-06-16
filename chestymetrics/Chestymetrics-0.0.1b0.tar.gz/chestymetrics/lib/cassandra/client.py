import click

from cassandra.cluster import Cluster
from cassandra.cluster import NoHostAvailable

from ..consumer.consumer import ConsumerClient
from ..rabbitmq.message import Message


class CassandraClient(ConsumerClient):

    def __init__(self, config):
        self.cluster = Cluster(
            contact_points=config.cassandra_endpoints.split(','),
            port=9042,
        )
        self.session = None

    def connect(self):
        if self.session and not self.session.is_shutdown:
            click.echo("already connected")

        try:
            self.session = self.cluster.connect(keyspace='metrics')
        except NoHostAvailable as e:
            click.echo(
                "\nError....couldn't connect to Cassandra"
            )
            raise e

    def disconnect(self):
        self.cluster.shutdown()

    def __del__(self):
        self.disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def recieve_message(self, message):
        for hostname, metrics in message.items():
            messages = [Message(**metric) for metric in metrics]

            for message in messages:
                bucket_time = ':'.join(message.time.split(':')[:-1])[:-1]+'0'
                self.session.execute(
                    """
                    INSERT INTO metrics.raw (host, service, bucket_time, time, metric)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (hostname, message.service, bucket_time, message.time, message.metric)
                )
