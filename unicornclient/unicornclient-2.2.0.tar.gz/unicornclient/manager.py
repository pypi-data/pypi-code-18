import importlib
import logging

from . import config
from . import spy

class Manager(object):
    def __init__(self, sender):
        logging.info('creating manager')
        self.sender = sender

        self.threads_to_start = config.DEFAULT_ROUTINES
        serial = spy.get_serial()
        if serial in config.CUSTOM_ROUTINES:
            self.threads_to_start.extend(config.CUSTOM_ROUTINES[serial])

        self.threads = {}

    def start(self):
        for thread in self.threads_to_start:
            logging.info("starting routine " + str(thread))
            module = importlib.import_module('unicornclient.routines.' + thread)
            routine = module.Routine()
            routine.manager = self
            routine.daemon = True
            routine.start()
            self.threads[thread] = routine

    def join(self):
        for thread in self.threads.values():
            thread.join()

    def forward(self, thread_name, task):
        if thread_name in self.threads:
            self.threads[thread_name].queue.put(task)

    def send(self, message):
        self.sender.send(message)

    def authenticate(self):
        self.forward('auth', True)
