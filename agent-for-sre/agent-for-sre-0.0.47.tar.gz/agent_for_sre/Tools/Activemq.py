#!/usr/bin/python
# encoding: utf-8
import time
import os
import stomp

class Activemq:
        def __init__(self, ip, port, user, password, topic, msg):
                self.ip = ip
                self.port = port
                self.user = user
                self.password = password
                self.topic = topic
                self.msg = msg

        def sendMessage(self):
                conn = stomp.Connection(host_and_ports=[(self.ip, self.port)])
                conn.start()
                conn.connect(self.user, self.password, wait=True)
                conn.send(body=self.msg, destination=self.topic)
                conn.disconnect()
