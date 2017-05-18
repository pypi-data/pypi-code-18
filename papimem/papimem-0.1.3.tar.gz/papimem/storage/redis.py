import logging
import pickle

import dsnparse
import redis

from .base import StorageBase


DEFAULT_DSN = 'redis://localhost:6379/0'


class RedisStorage(StorageBase):
    """ Redis storage implementation """

    def __init__(self, *args, **kwargs):
        super(RedisStorage, self).__init__(*args, **kwargs)
        dsn = kwargs.get('dsn', DEFAULT_DSN)
        dsnp = dsnparse.parse(dsn)
        self.redis = redis.StrictRedis(
            host=dsnp.host, port=dsnp.port, db=dsnp.paths[0]
        )

    def get(self, key):
        obj = self.redis.get(key)
        try:
            return pickle.loads(obj)
        except TypeError:
            logging.error('Unpickling Fails. No response found in storage.')
            return None

    def save(self, key, reqres):
        obj = pickle.dumps(reqres)
        return self.redis.set(key, obj)

    def get_all(self):
        for key in self.redis.scan_iter("*"):
            yield pickle.loads(self.redis.get(key))
