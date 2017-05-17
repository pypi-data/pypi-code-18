"""
LambdaSentryHandler

The way that raven records entries to Sentry by default is to use a threaded
model. Where the main thread will pass an exception to a thread for reporting.

In the lambda model, this means that we can miss some reports because the container
can get shutdown before the thread is done reporting.

Additionally, we don't want to record exceptions on the main thread in a sync manner.

There for, we will write the exception out to the task queue, to be recorded in the background.

"""

from __future__ import absolute_import
from __future__ import print_function

import logging

from raven.base import Client
from raven.handlers.logging import SentryHandler
from raven.transport.requests import RequestsHTTPTransport

from xavier.active import get_active_brain
from xavier.taskqueue import Task

logger = logging.getLogger(__name__)


SENTRY_CLIENT = None
IN_SENTRY_REPORTER = False


def get_sentry_client():
    global SENTRY_CLIENT
    if not SENTRY_CLIENT:
        sentry_dsn = get_active_brain().env.get('SENTRY_DSN')
        SENTRY_CLIENT = Client(sentry_dsn, transport=RequestsHTTPTransport)

    return SENTRY_CLIENT


def _record_sentry_exception(*args, **kwargs):
    global IN_SENTRY_REPORTER

    IN_SENTRY_REPORTER = True

    client = get_sentry_client()

    client.capture(*args, **kwargs)


record_sentry_exception = Task(_record_sentry_exception)


def sentry_lambda_wrapper(func):

    def _inside(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            logger.excepton("uncaught exception", exc)
            raise

    return _inside


class LambdaSentryHandler(SentryHandler):
    def __init__(self, *args, **kwargs):
        self.client = get_sentry_client()
        self.client.capture = record_sentry_exception.delay
        self.tags = kwargs.pop('tags', None)

        logging.Handler.__init__(self, level=kwargs.get('level', logging.NOTSET))

    def can_record(self, record):
        if IN_SENTRY_REPORTER:
            return False

        return super(LambdaSentryHandler, self).can_record(record)
