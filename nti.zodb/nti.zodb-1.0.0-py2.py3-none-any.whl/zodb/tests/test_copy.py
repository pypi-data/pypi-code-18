#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest import assert_that
from hamcrest import is_

import unittest

from nti.zodb.tests import SharedConfiguringTestLayer

from zope import copy
from persistent.wref import WeakRef
from persistent import Persistent
from ZODB import DB

class TestCopyWref(unittest.TestCase):

    def make_one(self):
        db = DB(None)
        conn = db.open()
        pers = Persistent()
        conn.add(pers)

        orig_wref = WeakRef(pers)

        return orig_wref

    def test_copy(self):
        # When not configured, can't copy the connection
        import pickle
        orig_wref = self.make_one()
        self.assertRaises(Exception, copy.copy, orig_wref)

class TestCopyFactory(TestCopyWref):

    layer = SharedConfiguringTestLayer

    def test_copy(self):
        orig_wref = self.make_one()

        wref2 = copy.copy(orig_wref)

        assert_that(wref2, is_(WeakRef))
        self.assertIsNot(orig_wref, wref2)
