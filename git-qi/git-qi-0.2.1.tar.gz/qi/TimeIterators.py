""" Iterators used to select times with which to search Git history. """

from datetime import datetime
from time import mktime
from dateutil.relativedelta import relativedelta as td, FR

def endhour(D):
    return D.replace(minute=59, second=59, microsecond=999999)

def endday(D):
    return endhour(D.replace(hour=23))

def endweek(D):
    return endday(D + td(weekday=FR(-1)))

def endmonth(D):
    return endday(D.replace(day=1) + td(months=1)  - td(days=1))

def endyear(D):
    return endday(D.replace(month=12, day=31))

def timeiter(epoch, start, cb, d):
    """ Generator used to select moments in time """
    e = datetime.utcfromtimestamp(int(epoch))
    s = datetime.utcfromtimestamp(int(start))
    while s > e:
        s = cb(s)
        yield int(mktime(s.timetuple()))
        s = s - d

def months(epoch, start):
    return timeiter(epoch, start, endmonth, td(months=1))

def weeks(epoch, start):
    return timeiter(epoch, start, endweek, td(weeks=1))

def days(epoch, start):
    return timeiter(epoch, start, endday, td(days=1))

def hours(epoch, start):
    return timeiter(epoch, start, endhour, td(hours=1))

def years(epoch, start):
    return timeiter(epoch, start, endyear, td(years=1))
