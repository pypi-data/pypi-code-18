#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# pylint: disable=protected-access

from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import has_length
from hamcrest import is_

import unittest
from zope.testing.loggingsupport import InstalledHandler

from nti.zodb.activitylog import AbstractActivityMonitor as ActivityMonitor
from nti.zodb.activitylog import LogActivityMonitor
from nti.zodb.activitylog import StatsdActivityMonitor

class TestBase(unittest.TestCase):

    def test_delegate_properties(self):

        class Base(object):
            b = 1

        base = Base()
        mon = ActivityMonitor(base)

        assert_that(mon, has_property('b', 1))

    def test_closedConnection(self):
        class Conn(object):
            loads = 1
            stores = 2
            database_name = 'DB'
            def db(self):
                return self
            def getTransferCounts(self, clear=False):
                l, s = self.loads, self.stores
                if clear:
                    self.loads = self.stores = 0
                return l, s

        class M(ActivityMonitor):
            def _closedConnection(self, loads, stores, db_name):
                assert_that(loads, is_(1))
                assert_that(stores, is_(2))
                assert_that(db_name, is_(Conn.database_name))

        mon = M(M())
        conn = Conn()
        mon.closedConnection(conn)

        assert_that(conn.loads, is_(0))
        assert_that(conn.stores, is_(0))

class TestLogActivityMonitor(unittest.TestCase):

    def setUp(self):
        super(TestLogActivityMonitor, self).setUp()
        self.handler = InstalledHandler('nti.zodb.activitylog')
        self.addCleanup(self.handler.uninstall)

    def test_closed_connection(self):

        mon = LogActivityMonitor()
        mon._closedConnection(1, 1, 'foo')

        assert_that(self.handler.records, has_length(1))

class TestStatsdLogActivityMonitor(unittest.TestCase):

    def test_closed_connection_no_client(self):
        mon = StatsdActivityMonitor()
        mon.statsd_client = lambda: None
        mon._closedConnection(1 , 1, 'foo')

    def test_closed_connection_with_client(self):
        glob_buf = []
        class MockClient(object):
            def gauge(self, key, value, buf):
                buf.append((key, value))
            def sendbuf(self, buf):
                glob_buf.extend(buf)

        mon = StatsdActivityMonitor()
        mon.statsd_client = MockClient
        mon._closedConnection(1 , 1, 'foo')
        assert_that(glob_buf,
                    is_([('ZODB.DB.foo.loads', 1),
                         ('ZODB.DB.foo.stores', 1)]))

class TestRegisterSubscriber(unittest.TestCase):

    def test_execute(self):
        from zope.processlifetime import DatabaseOpenedWithRoot
        from nti.zodb.activitylog import register_subscriber

        class DB(object):
            dam = None

            def __init__(self):
                self.databases = {'': self}
            def getActivityMonitor(self):
                return self.dam

            def setActivityMonitor(self, dam):
                self.dam = dam

        db = DB()
        event = DatabaseOpenedWithRoot(db)

        register_subscriber(event)

        dam = db.getActivityMonitor()
        assert_that(dam, is_(StatsdActivityMonitor))
        assert_that(dam, has_property('_base', is_(LogActivityMonitor)))
