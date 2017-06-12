# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil.relativedelta import relativedelta as rd
import calendar

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = DATE_FORMAT + ' %H:%M:%S'
LEN_DATETIME, LEN_DATE = 19, 10

class Date:
    def __init__(self, dt):
        if isinstance(dt, datetime):
            dt = dt.strftime(DATETIME_FORMAT)
        if isinstance(dt, date):
            dt = dt.strftime(DATE_FORMAT)
        assert len(dt) in [LEN_DATE, LEN_DATETIME], 'the format is not supported'
        self.is_date = len(dt) == LEN_DATE
        if self.is_date:
            self.dt = datetime.strptime(dt, DATE_FORMAT)
        self.is_datetime = len(dt) == LEN_DATETIME
        if self.is_datetime:
            self.dt = datetime.strptime(dt, DATETIME_FORMAT)

    def relativedelta(self, years=0, months=0, days=0, leapdays=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0, year=None, month=None, day=None, weekday=None, yearday=None, nlyearday=None, hour=None, minute=None, second=None, microsecond=None, last_day=False, rtype=None):
        assert rtype in [None, 'date', 'datetime'], 'the rtype should be date or datetime'
        if rtype:
            self.is_date = rtype == 'date'
            self.is_datetime = rtype == 'datetime'
        self.dt = self.dt + rd(years=years, months=months, days=days, leapdays=leapdays, weeks=weeks, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds, year=year, month=month, day=day, weekday=weekday, yearday=yearday, nlyearday=nlyearday, hour=hour, minute=minute, second=second, microsecond=microsecond)
        if last_day:
            day = calendar.monthrange(self.dt.year, self.dt.month)[1]
            self.dt = self.dt + rd(day=day)
        if self.is_date:
            return self.dt.strftime(DATE_FORMAT)
        if self.is_datetime:
            return self.dt.strftime(DATETIME_FORMAT)
