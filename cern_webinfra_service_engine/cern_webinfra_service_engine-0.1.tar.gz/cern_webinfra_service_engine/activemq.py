import os
import time
import stomp
import logging
import re

MyService = None
mf_config = {
    {
        'host': os.environ["AMQ_ADDRESS"],
        'port': os.environ["AMQ_PORT"],
        'user': os.environ["AMQ_USER"],
        'password': os.environ["AMQ_PASSWORD"],
        'destination': os.environ["AMQ_DESTINATION"]
    }
}


class Stomp(object):
    _connection = None

    def connect(self):
        self._connection = \
            stomp.Connection([(mq_config['host'], mq_config['port'])])
        while not self._connection.is_connected():
            self._connection.set_listener('', Consumer(self._connection))
            self._connection.start()
            self._connection.connect(mq_config['user'],
                                     mq_config['password'],
                                     wait=True)
        self._subscribe()
        time.sleep(60 * 60)
        self._connection.disconnect()

    def _subscribe(self):
        self._connection.subscribe(destination=mq_config['destination'],
                                   id=1,
                                   ack='auto')


class Consumer(stomp.ConnectionListener):
    def __init__(self, conn):
        self.app = MyService(conn)

    def on_error(self, headers, message):
        raise stomp.StompException(headers, message)

    def on_message(self, headers, message):
        self.app.process(headers, message)

    def on_disconnected(self):
        create_queue().connect()


def create_queue(Resources):
    MyService = Resources
    return Stomp()
