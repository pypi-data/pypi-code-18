# -*- coding: UTF-8 -*-

from datetime import date

from romme.conversion import republican_to_gregorian, gregorian_to_republican
from romme.names import republican_day_string
from romme.parse import parse_date

__all__ = ["RepublicanDate"]


def _cmp(a, b):
    """
    Port of Python 2's cmp function.
    """
    # https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons
    return (a > b) - (a < b)


class RepublicanDate:
    """
    Representation of a date in the French Republican calendar.
    """

    @classmethod
    def from_gregorian(cls, year, month, day):
        """
        Create a ``RepublicanDate`` from the given Gregorian year/month/day.
        ``from_gregorian(2017, 1, 1)`` converts the 1st of January, 2017.
        """
        return cls(*gregorian_to_republican(year, month, day))

    @classmethod
    def from_date(cls, d):
        """
        Create a ``RepublicanDate`` from the given ``datetime.date`` object.
        """
        return cls.from_gregorian(d.year, d.month, d.day)

    @classmethod
    def from_string(cls, s):
        """
        Return a ``RepublicanDate`` from a string, or ``None`` if it can't
        parse it.
        """
        ymd = parse_date(s)
        if ymd:
            return cls(*ymd)

    def __init__(self, year, month, day):
        """
        Create a new date. The day, month, and year should be given as
        numbers.
        - The day is an integer between 1 and 30 (included).
        - The month is an integer between 1 and 13 (included). Althought the
          calendar only has twelve months we use a third one for the
          "Sans-culottides", the days that were added at the end of each year
          to match the solar year.
        - The year is an integer starting from 1. Note there's no "Year Zero"
          in this calendar.
        """
        self.year = year
        self.month = month
        self.day = day

        self._ymd = (self.year, self.month, self.day)

    def is_sanscullotide(self):
        """
        Test if this date is a sans-culottide day.
        """
        return self.month == 13

    def to_date(self):
        """
        Return a ``datetime.date`` object for this date.
        """
        return date(*self.to_gregorian())

    def to_gregorian(self):
        """
        Return a ``(year, month, day)`` tuple that represents the date in the
        Gregorian calendar. The 1st of January, 2017 is represented as
        ``(2017, 1, 1)``.
        """
        return republican_to_gregorian(*self._ymd)

    def __str__(self):
        return republican_day_string(self.year, self.month, self.day)

    def __repr__(self):
        cls = self.__class__
        return "<%s.%s year=%d month=%d day=%d>" % (
            cls.__module__,
            cls.__name__,
            self.year,
            self.month,
            self.day)

    def _cmp(self, other):
        if isinstance(other, RepublicanDate):
            return _cmp(self._ymd, other._ymd)

        if isinstance(other, tuple) and len(other) == 3:
            return _cmp(self._ymd, other)

        if isinstance(other, date):
            return _cmp(self.to_date(), other)

        raise TypeError("Can't compare %s with a RepublicanDate" % repr(other))

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __le__(self, other):
        return self._cmp(other) < 1

    def __lt__(self, other):
        return self._cmp(other) == -1

    def __ge__(self, other):
        return self._cmp(other) > -1

    def __gt__(self, other):
        return self._cmp(other) == 1
