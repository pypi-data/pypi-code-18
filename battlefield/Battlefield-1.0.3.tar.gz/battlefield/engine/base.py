# -*- coding: utf-8 -*-
import json
import multiprocessing as mp
import socket

import pika

from . import Config, Robot


class Engine(object):
    """
    Engine is the base class of a game engine that creates a connection to a
    rabbitMQ and is able to send message to a queue and also create the 
    robots processes and starts them on running the engine.
    """

    PREFIX = 'BATTLEFIELD'

    def __init__(self, *args):
        self.conf = Config(Engine.PREFIX)

        self._mq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.conf.MQ_HOST,
                virtual_host=self.conf.MQ_VHOST,
                credentials=pika.PlainCredentials(
                    username=self.conf.MQ_USERNAME,
                    password=self.conf.MQ_PASSWORD
                )
            ),
        )

        self._mq_channel = self._mq_connection.channel()
        self._mq_channel.basic_qos(prefetch_count=1)
        self._mq_channel.queue_declare(queue=self.conf.MQ_QUEUE)

        self.robots = []
        for item in args:
            robot = Robot(item.id)
            robot.sock, item.sock = socket.socketpair()
            robot.process = mp.Process(target=item.run)
            robot.process.daemon = True
            self.robots.append(robot)

    def send(self, message):
        """
            sends a message to the queue.
        """
        self._mq_channel.basic_publish(exchange='',
                                       routing_key=self.conf.MQ_QUEUE,
                                       body=json.dumps(message))

    def run(self):
        """
        Runs the engine and also starts the robots processes.
        """
        for robot in self.robots:
            robot.process.start()
