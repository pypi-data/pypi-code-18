#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest import assert_that
from hamcrest import is_
from hamcrest import is_not
from hamcrest import same_instance
from nti.testing.matchers import validly_provides

from nti.wref.interfaces import ICachingWeakRef

from nti.zodb.wref import CopyingWeakRef

import unittest

from persistent import Persistent
from ZODB import DB
import transaction

class TestCopyWref(unittest.TestCase):

    def test_copy(self):
        db = DB(None)
        conn = db.open()
        pers = Persistent()
        conn.add(pers)
        conn.root()['a'] = pers

        orig_wref = CopyingWeakRef(pers)


        assert_that(orig_wref, validly_provides(ICachingWeakRef))
        assert_that(orig_wref(), is_(same_instance(pers)))

        del orig_wref._v_ob
        orig_wref.dm = {}

        assert_that(orig_wref(), is_not(same_instance(pers)))
