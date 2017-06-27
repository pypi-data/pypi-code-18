import json
import re
import sys

from sandpiper.concurrency import KeyLocker

try:
    import redis
except ImportError as e:
    raise ImportError('Failed to import "redis" ({})'.format(e))

from .abstract import Abstract
from .abstract import NonJSONStringError, SearchError

import logging

require_backward_compatibility = sys.version_info.major == 2


def create_client(**pool_args):
    if 'port' not in pool_args:
        pool_args['port'] = 6379

    if 'host' not in pool_args:
        raise ValueError('"host" is not defined.')

    pool = redis.ConnectionPool(**pool_args)

    return redis.Redis(connection_pool=pool)


class Adapter(Abstract):
    """ Adapter for Redis """
    def __init__(self, storage = None, namespace = None, delimiter = ':', auto_json_convertion = True):
        self._storage   = storage
        self._namespace = namespace or ''
        self._delimiter = delimiter

        self._re_namespace = re.compile('^{}:'.format(namespace))

        self._auto_json_convertion = auto_json_convertion

        self._key_locker = KeyLocker()

    @property
    def api(self):
        return self._storage

    def get(self, key):
        actual_key = self._actual_key(key)
        value      = self._key_locker.synchronize(None, self._storage.get, actual_key)

        if not value:
            return value

        if not self._auto_json_convertion:
            return value

        try:
            if not require_backward_compatibility and not isinstance(value, bytes):
                raise NonJSONStringError('Unable to decode the value (preemptive, py3, bytes)', value)

            if isinstance(value, bytes):
                return json.loads(value.decode('utf-8'))

            # NOTE This is mainly to support Python 2.
            if not isinstance(value, str):
                raise NonJSONStringError('Unable to decode the value (preemptive)', value)

            return json.loads(value)
        except json.decoder.JSONDecodeError:
            raise NonJSONStringError('Unable to decode the value (final)', value)

    def set(self, key, value, ttl = None):
        actual_key = self._actual_key(key)

        encoded = value

        if self._auto_json_convertion:
            encoded = json.dumps(value)

        self._key_locker.synchronize(None, self._storage.set, actual_key, encoded)

        if ttl != None and ttl > 0:
            self._storage.expire(actual_key, ttl)

    def remove(self, key):
        actual_key = self._actual_key(key)

        self._key_locker.synchronize(None, self._storage.delete, actual_key)

    def find(self, pattern='*', only_keys=False, ignore_non_decodable=True):
        actual_pattern = self._actual_key(pattern)

        keys = []

        if require_backward_compatibility:
            keys.extend([
                self._re_namespace.sub('', key)
                for key in self._storage.keys(actual_pattern)
            ])
        else:
            keys.extend([
                self._re_namespace.sub('', key.decode('utf-8'))
                for key in self._storage.keys(actual_pattern)
                if isinstance(key, bytes)
            ])

        if only_keys:
            return keys

        result = {}

        for key in keys:
            data = None

            try:
                data = self.get(key)
            except NonJSONStringError:
                if not ignore_non_decodable:
                    raise SearchError(pattern)
                # endif

            result[key] = data

        return result

    def _actual_key(self, key):
        if not self._namespace:
            return key

        return '{}{}{}'.format(self._namespace, self._delimiter, key)
