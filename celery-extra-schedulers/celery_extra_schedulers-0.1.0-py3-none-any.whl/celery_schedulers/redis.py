import pickle

from celery.beat import Scheduler
from celery.utils.log import get_logger
from redis import StrictRedis

logger = get_logger(__name__)


class RedisScheduler(Scheduler):
    """
    Celery redis scheduler.
    """

    def __init__(self, app, *args, **kwargs):
        self.rdb = StrictRedis.from_url(app.conf.CELERY_BEAT_REDIS_URL)

        super().__init__(app, *args, **kwargs)

    def setup_schedule(self):
        self.merge_inplace(self.app.conf.CELERY_BEAT_SCHEDULE)
        self.install_default_entries(self.schedule)

        schedule = self.rdb.get('celery:schedule')
        if schedule:
            schedule = pickle.loads(schedule)
            self.update_from_dict(schedule)

        self.sync()

    def sync(self):
        self.rdb.set('celery:schedule', pickle.dumps(self.schedule))


class RedisMultiScheduler(RedisScheduler):
    """
    Celery redis multi-scheduler.
    
    Only single instance of running beat instances will be active.
    """

    lock = None

    def __init__(self, app, *args, **kwargs):
        self.lock_ttl = getattr(app.conf, 'CELERY_BEAT_LOCK_TTL', 60)

        super().__init__(app, *args, **kwargs)

    def acquire_lock(self):
        lock = self.rdb.lock('celery:lock', timeout=self.lock_ttl, sleep=1)

        if lock.acquire(blocking=False):
            self.lock = lock
            logger.info('beat: lock acquired.')
            return True

        logger.info('beat: another beat instance already running. awaiting...')

        return False

    def renew_lock(self):
        self.rdb.pexpire('celery:lock', self.lock_ttl * 1000)

        logger.info('beat: lock renewed.')

    def release_lock(self):
        self.lock.release()
        self.lock = None

    def setup_schedule(self):
        self.acquire_lock()

        super().setup_schedule()

    def tick(self, *args, **kwargs):
        if not self.lock:
            if not self.acquire_lock():
                return self.max_interval
        else:
            self.renew_lock()

        return super().tick(*args, **kwargs)

    def sync(self):
        if not self.lock:
            return

        super().sync()

    def close(self):
        super().close()

        if self.lock:
            self.release_lock()
