import json


class Consumer(object):
    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        for listener in self.listeners:
            listener.recieve_message(message)


class ConsumerClient(object):
    """
    template class for clients that consume messages to extend
    """
    def recieve_message(self, message):
        raise NotImplementedError()
