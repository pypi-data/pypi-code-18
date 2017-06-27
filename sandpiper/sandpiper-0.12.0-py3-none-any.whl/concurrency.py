import contextlib
import threading

DEFAULT_LOCK_ACQUISITION_TIME_LIMIT = 30


class ZombieStateError(RuntimeError):
    """ Unable to acquire lock within the limited timeframe """


class UnknownLockKeyError(RuntimeError):
    """ The lock key is unknown to the locker. """


class KeyLocker(object):
    """ Dynamic Lock Manager """
    def __init__(self, lock_acquistition_time_limit = None):
        self._key_management_lock          = threading.Lock()
        self._primary_lock                 = threading.Lock()
        self._lockers                      = dict()
        self._lock_acquistition_time_limit = lock_acquistition_time_limit or DEFAULT_LOCK_ACQUISITION_TIME_LIMIT

    def acquire(self, key = None, blocking = True, timeout = -1):
        lock = self._get_lock(key, dry_run = False)

        return lock.acquire(blocking, timeout = timeout)

    def release(self, key = None):
        lock = self._get_lock(key, dry_run = True)

        try:
            lock.release()
        except RuntimeError:
            pass # Probably try to release the unlocked lock.

    def synchronize(self, key, callback, *args, **kwargs):
        self.acquire(key)

        result = callback(*args, *kwargs)

        self.release(key)

        return result

    def _get_lock(self, key, dry_run):
        if not key:
            return self._primary_lock

        if not self._key_management_lock.acquire(timeout = self._lock_acquistition_time_limit):
            raise ZombieStateError('Failed to acquire the key management lock in time.')

        if key not in self._lockers:
            if dry_run:
                raise UnknownLockKeyError(key)

            self._lockers[key] = threading.Lock()

        try:
            self._key_management_lock.release()
        except RuntimeError:
            pass # Probably try to release the unlocked lock.

        return self._lockers[key]
