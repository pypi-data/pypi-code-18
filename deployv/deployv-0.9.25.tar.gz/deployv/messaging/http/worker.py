# coding: utf-8

from deployv.messaging.basemsg import BaseWorker
from deployv.base import errors
import logging
import signal


_logger = logging.getLogger('deployv')


def signal_handler(signal_number, stack_frame):
    raise errors.GracefulExit(
        'Received a signal to terminate, stopping workers'
    )


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


class HttpWorker(BaseWorker):
    def __init__(self, configuration_object, sender_class, receiver_class,
                 worker_id):
        super(HttpWorker, self).__init__(configuration_object, sender_class, receiver_class,
                                         worker_id)

    def run(self):
        """ Worker method, runs the method that performs a request to the odoo controller
        and retrieves the messages
        """
        _logger.info("W%s - waiting for something to do", self._wid)
        try:
            self._receiver.run(self.callback)
        except errors.GracefulExit:
            self.signal_exit()

    def signal_exit(self):
        """ Exit when finished with current loop """
        self._receiver.stop()

    def kill(self):
        """ This kill immediately the process, should not be used """
        self._receiver.stop()
        self.terminate()
        self.join()

    def callback(self, message):
        _logger.info('Received a message worker %s', self._wid)
        self.execute_rpc(message)
