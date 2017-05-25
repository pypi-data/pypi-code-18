# coding=utf8




class CacheBase(object):
    """
    缓存后端基类, 定义缓存的基本行为
    """
    def get_obj(self, key):
        pass

    def set_obj(self, key, value, expire):
        pass

    def clear(self, key):
        pass

class DummyBackend(CacheBase):
    """
    加装缓存了
    """
    def __init__(self):
        self.store = {}

    def get_obj(self, key):
        #print "get key", key
        if key in self.store:
            return self.store[key]
        return None

    def set_obj(self, key, value, expire):
        #print "set", key, "=", value
        self.store[key] = value

    def clear(self, key):
        del self.store[key]
