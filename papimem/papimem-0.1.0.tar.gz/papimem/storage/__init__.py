import sys
import logging

import dsnparse

from .redis import RedisStorage


STORAGE_REGISTRY = {
    'redis': RedisStorage,

    # Register other storages here
}


def get_storage(storage_dsn):
    """ Instantiate storage for given DSN """
    storage_scheme = dsnparse.parse(storage_dsn).scheme
    storage_cls = STORAGE_REGISTRY.get(storage_scheme)
    if not storage_cls:
        logging.error("Can't find storage for given dsn.")
        sys.exit(-1)
    return storage_cls(dsn=storage_dsn)
