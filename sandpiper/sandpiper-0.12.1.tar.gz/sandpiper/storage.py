from .adapter.abstract import NotSupported
from .adapter.inmemory import InMemory
from .concurrency      import KeyLocker
from .mixin            import DictionaryAccess


class Storage(DictionaryAccess):
    def __init__(self, driver = None):
        self.driver     = driver or InMemory()
        self.key_locker = KeyLocker()

    def get(self, key):
        return self.key_locker.synchronize(key, self.driver.get, key)

    def set(self, key, value, ttl = None):
        self.key_locker.synchronize(key, self.driver.set, key, value, ttl)

    def remove(self, key):
        self.key_locker.synchronize(key, self.driver.remove, key)

    def find(self, *args, **kwargs):
        try:
            return self.driver.find(*args, **kwargs)
        except NotSupported as e:
            return []
