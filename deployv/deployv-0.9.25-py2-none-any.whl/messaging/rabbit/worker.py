# coding: utf-8

from deployv.messaging.basemsg import BaseWorker
import logging
import signal
from deployv.base import errors


_logger = logging.getLogger('deployv')


def signal_handler(signal_number, stack_frame):
    raise errors.GracefulExit(
        'Received a signal to terminate, stopping workers'
    )


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


class RabbitWorker(BaseWorker):
    def __init__(self, configuration_object, sender_class, receiver_class,
                 worker_id):
        super(RabbitWorker, self).__init__(configuration_object, sender_class, receiver_class,
                                           worker_id)

    def run(self):
        """ Worker method, open a channel through a pika connection and
            start consuming
        """
        _logger.info("W%s - waiting for something to do", self._wid)
        try:
            self._receiver.run(self.callback)
        except errors.GracefulExit:
            self.signal_exit()

    def signal_exit(self):
        """ Exit when finished with current loop """
        try:
            self._receiver.stop()
        except errors.GracefulExit:
            _logger.info('Worker stopped')
        self.stop_working.set()

    def kill(self):
        """ This kill immediately the process, should not be used """
        self._receiver.stop()
        self.terminate()
        self.join()

    def callback(self, channel, method, properties, body):
        """ This method is executed as soon as a message arrives, according to the
            `pika documentation
            <http://pika.readthedocs.org/en/latest/examples/blocking_consume.html>`_. The
            parameters are fixed according to it, even if the are unused
        """
        _logger.info('Received a message worker %s', self._wid)
        message = self.check_message(body)
        if message:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            self.execute_rpc(body)
