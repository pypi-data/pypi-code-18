#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# pylint: disable=protected-access

from hamcrest import is_
from hamcrest import raises
from hamcrest import has_key
from hamcrest import calling
from hamcrest import less_than
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import greater_than
from hamcrest import same_instance
from hamcrest import less_than_or_equal_to

from nti.testing.matchers import validly_provides

import unittest
import pickle

from nti.zodb import interfaces
from nti.zodb.minmax import Maximum
from nti.zodb.minmax import Minimum
from nti.zodb.minmax import MergingCounter
from nti.zodb.minmax import NumericMaximum
from nti.zodb.minmax import NumericMinimum
from nti.zodb.minmax import ConstantZeroValue
from nti.zodb.minmax import NumericPropertyDefaultingToZero


class TestMinMax(unittest.TestCase):

    def test_zope_imports_have_set(self):
        for t in Minimum, Maximum:
            v = t(0)
            v.set(1)
            assert_that(v.value, is_(1))

    def test_comparisons(self):
        mc1 = MergingCounter()
        mc2 = MergingCounter()

        assert_that(mc1, is_(mc2))
        assert_that(mc1, validly_provides(interfaces.INumericCounter))

        mc2.increment()

        assert_that(mc1, is_(less_than(mc2)))
        assert_that(mc2, is_(greater_than(mc1)))

        mc1.increment()
        assert_that(mc1, is_(less_than_or_equal_to(mc2)))

        assert_that(hash(mc1), is_(mc1.value))

    def test_add(self):
        mc1 = MergingCounter(1)
        mc2 = MergingCounter(2)

        assert_that(mc1 + mc2, is_(MergingCounter(3)))

        assert_that(mc1 + 2, is_(3))

        mc1 += 2
        assert_that(mc1, is_(MergingCounter(3)))

    def test_merge_resolve(self):

        assert_that(MergingCounter()._p_resolveConflict(0, 0, 1), is_(1))
        # simultaneous increment adds
        assert_that(MergingCounter()._p_resolveConflict(0, 1, 1), is_(2))

    def test_min_resolve(self):

        assert_that(NumericMinimum()._p_resolveConflict(0, 0, 1), is_(0))
        # simultaneous increment adds
        assert_that(NumericMinimum()._p_resolveConflict(3, 4, 2), is_(2))

    def test_str(self):

        mc = MergingCounter()
        assert_that(str(mc), is_("0"))
        assert_that(repr(mc), is_("MergingCounter(0)"))

        mc.set(1)
        assert_that(str(mc), is_("1"))
        assert_that(repr(mc), is_("MergingCounter(1)"))

    def test_zero(self):
        czv = ConstantZeroValue()
        assert_that(czv, is_(same_instance(ConstantZeroValue())))
        assert_that(czv, has_property('value', 0))

        # equality
        assert_that(czv, is_(czv))
        v = NumericMaximum()
        assert_that(czv, is_(v))
        assert_that(v, is_(czv))

        v.value = -1
        assert_that(v, is_(less_than(czv)))

        v.value = 1
        assert_that(v, is_(greater_than(czv)))

        czv.value = 1
        assert_that(czv, has_property('value', 0))

        czv.set(2)
        assert_that(czv, has_property('value', 0))

        assert_that(calling(pickle.dumps).with_args(czv),
                    raises(TypeError))
        assert_that(calling(czv._p_resolveConflict).with_args(None, None, None),
                    raises(NotImplementedError))

from nti.zodb.persistentproperty import PersistentPropertyHolder

from ZODB import DB

class WithProperty(PersistentPropertyHolder):

    a = NumericPropertyDefaultingToZero(
        'a',
        NumericMaximum,
        as_number=True)
    b = NumericPropertyDefaultingToZero('b', MergingCounter)

class NPProperty(object):
    a = NumericPropertyDefaultingToZero(
        'a',
        NumericMaximum,
        as_number=True)
    b = NumericPropertyDefaultingToZero('b', MergingCounter)


class TestPropertyNonPersistent(unittest.TestCase):

    def make_one(self):
        obj = NPProperty()
        return obj

    def test_all_works(self):
        obj = self.make_one()

        assert_that(obj.a, is_(0))

        del obj.a
        assert_that(obj.a, is_(0))

        obj.a = 0
        assert_that(obj.a, is_(0))
        self.assertNotIn('a', obj.__dict__)

        obj.a = 1
        assert_that(obj.a, is_(1))

        obj.a = 2
        assert_that(obj.a, is_(2))

        del obj.a
        assert_that(obj.a, is_(0))

        assert_that(obj.b, is_(type(ConstantZeroValue())))

        # No change
        obj.b.set(0)
        assert_that(obj.b, is_(type(ConstantZeroValue())))


class TestProperty(TestPropertyNonPersistent):

    def make_one(self):
        db = DB(None)
        conn = db.open()

        obj = WithProperty()
        conn.add(obj)
        return obj

    def test_get_klass(self):
        assert_that(WithProperty.a, is_(NumericPropertyDefaultingToZero))

    def test_zero_property_increment(self):
        obj = self.make_one()

        assert_that(obj._p_status, is_('saved'))

        # Just accessing them doesn't change the saved status
        assert_that(obj.a, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.b.value, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.__getstate__(), is_({}))

        # Only when we do something does the status change
        obj.b.increment()
        assert_that(obj._p_status, is_('changed'))
        assert_that(obj.b, is_(same_instance(obj.b)))
        assert_that(obj.__getstate__(), has_key('b'))
        assert_that(obj.b, is_(MergingCounter))

    def test_zero_property_set(self):
        obj = self.make_one()

        assert_that(obj._p_status, is_('saved'))

        # Just accessing them doesn't change the saved status
        assert_that(obj.a, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.b.value, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.__getstate__(), is_({}))

        # Only when we do something does the status change
        obj.b.set(3)
        assert_that(obj._p_status, is_('changed'))
        assert_that(obj.b, is_(same_instance(obj.b)))
        assert_that(obj.__getstate__(), has_key('b'))
        assert_that(obj.b.value, is_(3))

    def test_zero_property_value(self):
        obj = self.make_one()

        assert_that(obj._p_status, is_('saved'))

        # Just accessing them doesn't change the saved status
        assert_that(obj.a, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.b.value, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.__getstate__(), is_({}))

        # Only when we do something does the status change
        obj.a = 3
        assert_that(obj._p_status, is_('changed'))
        assert_that(obj.a, is_(same_instance(obj.a)))
        assert_that(obj.__getstate__(), has_key('a'))
        assert_that(obj.a, is_(3))
