import pika
import os

class DQuotNotificationProviderRabbitMQ:
    def __init__(self, host = '127.0.0.1', port = 5672, vhost = '/'):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.connection = self.connection()

    def connection(self):
        credentials = pika.PlainCredentials(os.getenv('DQUOT_RABBITMQ_USER'),
                                            os.getenv('DQUOT_RABBITMQ_PASS'))
        parameters = pika.ConnectionParameters(self.host, self.port, self.vhost)
        return pika.BlockingConnection(parameters)

    def send(self, input):
        channel = self.connection.channel()
        channel.queue_declare(queue='quota.warnings')
        channel.basic_publish(exchange='helloEx', routing_key='', body='Hello World!')
        self.connection.close
