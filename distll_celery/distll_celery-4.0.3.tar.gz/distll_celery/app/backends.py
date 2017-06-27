# -*- coding: utf-8 -*-
"""Backend selection."""
from __future__ import absolute_import, unicode_literals
import sys
import types
from distll_celery.exceptions import ImproperlyConfigured
from distll_celery._state import current_app
from distll_celery.five import reraise
from distll_celery.utils.imports import load_extension_class_names, symbol_by_name

__all__ = ['by_name', 'by_url']

UNKNOWN_BACKEND = """
Unknown result backend: {0!r}.  Did you spell that correctly? ({1!r})
"""

BACKEND_ALIASES = {
    'amqp': 'distll_celery.backends.amqp:AMQPBackend',
    'rpc': 'distll_celery.backends.rpc.RPCBackend',
    'cache': 'distll_celery.backends.cache:CacheBackend',
    'redis': 'distll_celery.backends.redis:RedisBackend',
    'mongodb': 'distll_celery.backends.mongodb:MongoBackend',
    'db': 'distll_celery.backends.database:DatabaseBackend',
    'database': 'distll_celery.backends.database:DatabaseBackend',
    'elasticsearch': 'distll_celery.backends.elasticsearch:ElasticsearchBackend',
    'cassandra': 'distll_celery.backends.cassandra:CassandraBackend',
    'couchbase': 'distll_celery.backends.couchbase:CouchbaseBackend',
    'couchdb': 'distll_celery.backends.couchdb:CouchBackend',
    'riak': 'distll_celery.backends.riak:RiakBackend',
    'file': 'distll_celery.backends.filesystem:FilesystemBackend',
    'disabled': 'distll_celery.backends.base:DisabledBackend',
    'consul': 'distll_celery.backends.consul:ConsulBackend'
}


def by_name(backend=None, loader=None,
            extension_namespace='distll_celery.result_backends'):
    """Get backend class by name/alias."""
    backend = backend or 'disabled'
    loader = loader or current_app.loader
    aliases = dict(BACKEND_ALIASES, **loader.override_backends)
    aliases.update(
        load_extension_class_names(extension_namespace) or {})
    try:
        cls = symbol_by_name(backend, aliases)
    except ValueError as exc:
        reraise(ImproperlyConfigured, ImproperlyConfigured(
            UNKNOWN_BACKEND.strip().format(backend, exc)), sys.exc_info()[2])
    if isinstance(cls, types.ModuleType):
        raise ImproperlyConfigured(UNKNOWN_BACKEND.strip().format(
            backend, 'is a Python module, not a backend class.'))
    return cls


def by_url(backend=None, loader=None):
    """Get backend class by URL."""
    url = None
    if backend and '://' in backend:
        url = backend
        scheme, _, _ = url.partition('://')
        if '+' in scheme:
            backend, url = url.split('+', 1)
        else:
            backend = scheme
    return by_name(backend, loader), url
