import pika

from .rabbit_setting import no_ack
from .rabbit_setting import delivery_mode


class Rabbit:
    def __init__(self):
        self.connection = None
        self.no_ack = no_ack
        self.delivery_mode = delivery_mode

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    def disconnect(self):
        self.connection.close()

    def channel(self):
        return self.connection.channel()

    def queue(self,channel,queue_name):
        return channel.queue_declare(queue=queue_name)

    def queue_bind(self,channel,exchange,queue,binding_key=''):
        channel.queue_bind(exchange=exchange,
                           queue=queue.method.queue,
                           routing_key=binding_key)


    def publish(self,channel,exchange,routing_key,body):
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body,
                              properties=pika.BasicProperties(
                                  delivery_mode=self.delivery_mode,  # make message persistent
                              ))

    def consume(self,channel,callback,queue):
        channel.basic_consume(callback,
                              queue=queue,
                              no_ack=self.no_ack)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

