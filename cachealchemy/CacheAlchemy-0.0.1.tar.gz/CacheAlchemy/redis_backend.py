# coding=utf8
from CacheAlchemy.base_backend import CacheBase

class RedisBackend(CacheBase):
    def __init__(self, redis_conn):
        """
        通过一个redis连接来初始化缓存后端
        :param redis_conn: 
        :type redis_conn: 
        """
        self.redis = redis_conn

    def set_obj(self, key, value, expire=0):
        redis_key = "cached:key:%s" % key
        self.redis.set(redis_key, value)
        if expire:
            self.redis.expire(redis_key, expire)

    def clear(self, key):
        redis_key = "cached:key:%s" % key
        self.redis.delete(redis_key)

    def get_obj(self, key):
        redis_key = "cached:key:%s" % key
        return self.redis.get(redis_key)

