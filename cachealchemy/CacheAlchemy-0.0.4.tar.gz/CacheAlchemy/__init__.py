# coding=utf8


from cached import cached_by_id, init_cached , CachedQuery
from base_backend import CacheBase, DummyBackend
from redis_backend import RedisBackend