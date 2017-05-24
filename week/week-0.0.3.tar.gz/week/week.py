#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-09-18 11:36:43

import datetime
from datetime import date


class Week(object):
    """
        this first monday of a year starts the firt week.
        Every week starts from monday and end in sunday.
    """

    def __init__(self, year, week):
        """
            year: year
            week: week
        """
        assert 1970 < year < 9999
        assert 1 <= week <= 53
        self.year = year
        self.week = week

    @classmethod
    def create_from_date(cls, date_obj):
        """
            date: datetime.date
            example: week = Week.create_from_date(date(2016, 9, 18))
        """
        year = date_obj.year
        week = int(date_obj.strftime('%W'))
        if week == 0:
            date_obj = date(year - 1, 12, 31)
            return cls.create_from_date(date_obj=date_obj)
        week_obj = cls(year=date_obj.year, week=week)
        return week_obj

    @property
    def startdate(self):
        new_years_day = date(year=self.year, month=1, day=1)
        startdate = new_years_day + \
            datetime.timedelta(days=(7 - new_years_day.weekday()) % 7) + \
            datetime.timedelta(days=(self.week - 1) * 7)
        return startdate

    @property
    def startdatetime(self):
        return datetime.datetime.strptime(
            self.startdate.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    @property
    def enddate(self):
        enddate = self.startdate + datetime.timedelta(days=6)
        return enddate

    @property
    def enddatetime(self):
        return datetime.datetime.strptime(
            self.enddate.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S") +\
            datetime.timedelta(days=0, seconds=3600 * 24)

    def next_week(self):
        return Week.create_from_date(self.startdate + datetime.timedelta(days=7))

    def get_year_week(self):
        week = "%d%02d" % (self.year, self.week)
        return week

    def __str__(self):
        return "{0}year {1}week".format(self.year, self.week)

    def get_next_week(self):
        """return next week"""
        return Week.create_from_date(
            self.startdate + datetime.timedelta(days=7))

    def get_previous_week(self):
        """return previous week"""
        return Week.create_from_date(
            self.startdate - datetime.timedelta(days=7))

    @classmethod
    def thisweek(self):
        return self.create_from_date(datetime.date.today())

    def __add__(self, integer):
        """n week later"""
        return Week.create_from_date(
            self.startdate + datetime.timedelta(days=7*integer))

    def __sub_integer__(self, integer):
        """n week previous"""
        return Week.create_from_date(
            self.startdate - datetime.timedelta(days=7*integer))

    def __gt__(self, week):
        if self.year > week.year:
            return True
        elif self.year < week.year:
            return False
        else: return self.week > week.week

    def __sub__(self, week):
        """calculate the period of two week instance"""
        if isinstance(week, int):
            return self.__sub_integer__(week)
        return (self.startdate - week.startdate).days/7

    def __eq__(self, week):
        return self.get_year_week() == week.get_year_week()
