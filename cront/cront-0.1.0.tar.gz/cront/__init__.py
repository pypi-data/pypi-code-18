import traceback
import datetime
import logging

from tornado.gen import coroutine, Task
from tornado.ioloop import IOLoop

__all__ = ['cron_task']

version = "0.1.0"


logger = logging.getLogger(__name__)


class CronTask(object):

    def __init__(self, func, param):
        """
        :param func:
        :param param: minute hour  day   month  weekday
                      0-59   0-23  1-31  1-12   1-7 (Monday=1)
        """
        def str2list(s, start, stop):
            r = set()
            for i in s.split(','):
                if i.isdigit():
                    r.add(int(i))
                else:
                    i = i.replace('*', '%s-%s' % (start, stop))
                    if '/' not in i:
                        i += '/1'
                    sp0, divider = i.split('/')
                    if '-' in sp0:
                        sp1, sp2 = sp0.split('-')
                        divider = int(divider)
                        r.update([j for j in range(int(sp1), int(sp2) + 1) if not j % divider])
            return sorted(list(r))

        self.func = func
        self.func_name = func.__name__
        minute, hour, day, month, weekday = ([i for i in param.split(' ') if i] + ['*'] * 5)[:5]
        self.temp = [str2list(weekday, 1, 7),
                     str2list(month, 1, 12),
                     str2list(day, 1, 31),
                     str2list(hour, 0, 23),
                     str2list(minute, 0, 59)]

    def _schedule_next(self, first=False):
        def _find(n):
            if d[n] in self.temp[n]:
                return d[n], False, False
            for k, j in enumerate(self.temp[n]):
                if j >= d[n]:
                    return self.temp[n][k], False, self.temp[n][k] != d[n]
            return self.temp[n][0], True, self.temp[n][0] != d[n]

        def _d_month():
            if d[1] < 12:
                x = datetime.date(d[0], d[1] + 1, 1)
            else:
                x = datetime.date(d[0] + 1, 1, 1)
            return (x - datetime.timedelta(days=1)).day

        def clear(n):
            if n < 2:
                d[1] = self.temp[1][0]
            if n < 3:
                d[2] = self.temp[2][0]
            if n < 4:
                d[3] = self.temp[3][0]
            if n < 5:
                d[4] = self.temp[4][0]

        def mk(n):
            d[n], _over, ch = _find(n)
            if _over:
                d[n - 1] += 1
                clear(n)
            if ch and n < 4:
                clear(n)
                return True

            if n == 2 and d[2] > _d_month():
                d[1] += 1
                clear(n)
                return True

        t = datetime.datetime.now()
        t1 = t + datetime.timedelta(minutes=(2 if first else 1))
        d = [t1.year, t1.month, t1.day, t1.hour, t1.minute]
        over = True
        while over:
            for i in range(4, 0, -1):
                if mk(i):
                    break
            else:
                over = not datetime.date(d[0], d[1], d[2]).isoweekday() in self.temp[0]
                if over:
                    d[2] += 1
                    clear(3)
        return datetime.datetime(*d) - t

    @coroutine
    def run(self, app):
        x = self._schedule_next(first=True)
        logger.debug('NEXT CRON TASK %s %s' % (x, self.func_name))
        while True:
            yield Task(IOLoop.current().add_timeout, x)
            logger.info('RUN CRON TASK %s' % self.func_name)
            try:
                self.func(app)
                logger.info('END CRON TASK %s' % self.func_name)
            except Exception:
                logger.error(traceback.format_exc())

            x = self._schedule_next()
            logger.debug('NEXT CRON TASK %s %s' % (x, self.func_name))


class CronTaskDecorator(object):
    _instance = None
    tasks = []

    def __new__(cls, param):
        if not cls._instance:
            cls._instance = super(CronTaskDecorator, cls).__new__(cls)

        cls._instance.param = param
        return cls._instance

    def __call__(self, func):
        self.tasks.append(CronTask(func, self.param))
        return func

    @classmethod
    def start(cls, app):
        for tsk in cls.tasks:
            tsk.run(app)

cron_task = CronTaskDecorator
