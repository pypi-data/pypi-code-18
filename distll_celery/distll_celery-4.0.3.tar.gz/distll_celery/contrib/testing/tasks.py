"""Helper tasks for integration tests."""
from __future__ import absolute_import, unicode_literals
from distll_celery import shared_task


@shared_task(name='distll_celery.ping')
def ping():
    # type: () -> str
    """Simple task that just returns 'pong'."""
    return 'pong'
