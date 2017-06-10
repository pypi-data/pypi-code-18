# -*- coding: UTF-8 -*-

import jdcal


# These constants as well as the calculation below are based off PHP's
# SdnToFrench and FrenchToSdn functions in ext/calendar/french.c:
#   https://github.com/php/php-src/blob/6053987/ext/calendar/french.c
_DAYS_PER_4_YEARS = 365 * 4 + 1
_DAYS_PER_MONTH = 30
_FRENCH_JDN_OFFSET = 2375474

def _republican_ymd_to_julian_day(y, m, d):
    """
    Convert a ``(year, month, day)`` tuple of the French Republican calendar
    into a Julian day number.
    """
    yd = int((y * _DAYS_PER_4_YEARS) / 4)
    return yd + (m-1) * _DAYS_PER_MONTH + d + _FRENCH_JDN_OFFSET

def _julian_day_to_republican_ymd(jd):
    """
    Convert a Julian day number to a ``(year, month, day)`` tuple representing
    the date in the French Republican calendar.
    """
    days4 = (int(jd) - _FRENCH_JDN_OFFSET) * 4 - 1

    y, day_of_year = divmod(days4, _DAYS_PER_4_YEARS)

    day_of_year /= 4

    m, d = divmod(day_of_year, _DAYS_PER_MONTH)

    # Start months and days at 1 instead of 0
    m += 1
    d += 1

    return (int(y), int(m), int(d))


def republican_to_gregorian(y, m, d):
    """
    Take a year (y>=1), a month (1<=m<=13), and a day (1<=d<=30) that represent
    a day from the French Republican calendar and return a (year, month, day)
    tuple that represent the same date in the Gregorian calendar.
    """
    y, m, d, _ = jdcal.jd2gcal(0, _republican_ymd_to_julian_day(y, m, d))
    return (y, m, d)


def gregorian_to_republican(y, m, d):
    """
    Take a year (y>=1792), a month (1<=m<=12), and a day (1<=d<=31) that
    represent a day from the Gregorian calendar and return a tuple that
    represent the same date in the French Republican calendar.
    """
    jd = sum(jdcal.gcal2jd(y, m, d))
    jd = int(jd + 1) # ceil

    return _julian_day_to_republican_ymd(jd)
