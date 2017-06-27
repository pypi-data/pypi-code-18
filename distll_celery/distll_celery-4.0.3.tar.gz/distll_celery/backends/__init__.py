"""Result Backends."""
from __future__ import absolute_import, unicode_literals
from distll_celery.app import backends as _backends
from distll_celery.utils import deprecated


@deprecated.Callable(
    deprecation='4.0',
    removal='5.0',
    alternative='Please use distll_celery.app.backends.by_url')
def get_backend_cls(backend=None, loader=None, **kwargs):
    """Deprecated alias to :func:`distll_celery.app.backends.by_name`."""
    return _backends.by_name(backend=backend, loader=loader, **kwargs)


@deprecated.Callable(
    deprecation='4.0',
    removal='5.0',
    alternative='Please use distll_celery.app.backends.by_url')
def get_backend_by_url(backend=None, loader=None):
    """Deprecated alias to :func:`distll_celery.app.backends.by_url`."""
    return _backends.by_url(backend=backend, loader=loader)
