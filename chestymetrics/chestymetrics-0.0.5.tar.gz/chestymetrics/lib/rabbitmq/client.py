import pika


class RabbitMQClient(object):
    def __init__(self, config):
        self.queue = config.rabbitmq_queue
        self.exchange = config.rabbitmq_exchange
        self.host = config.rabbitmq_host
        self.type = None

    def __enter__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()


class RabbitMQPublisher(RabbitMQClient):
    def push_message(self, body):
        if not self.type:
            self.set_publisher()
        assert self.type == 'publisher'
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=body)

    def set_publisher(self):
        self.channel.queue_declare(queue=self.queue)
        self.type = 'publisher'


class RabbitMQConsumer(RabbitMQClient):
    def consume(self, callback):
        self.channel.basic_consume(callback, queue=self.queue, no_ack=True)
        self.channel.start_consuming()

