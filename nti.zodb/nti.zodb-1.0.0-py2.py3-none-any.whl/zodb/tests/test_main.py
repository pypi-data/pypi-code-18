#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from zope import interface
from ZODB.interfaces import IBroken

from hamcrest import assert_that
from hamcrest import has_property
from nti.testing.matchers import is_false
from nti.testing.matchers import is_true

import unittest

from nti.zodb import readCurrent
from nti.zodb import isBroken

class TestReadCurrent(unittest.TestCase):

    def test_activate_missing(self):
        readCurrent(self)

    def test_activate_but_no_jar(self):
        class O(object):
            activated = False
            def _p_activate(self):
                self.activated = True

        o = O()
        readCurrent(o)
        assert_that(o, has_property('activated', True))

    def test_activate_with_jar(self):
        class O(object):
            def __init__(self):
                self._p_jar = self
                self.current = []
                self.readCurrent = self.current.append

            def _p_activate(self):
                pass


        o = O()
        readCurrent(o)
        assert_that(o, has_property('current', [o]))

    def test_container(self):
        class Base(object):
            def __init__(self, data):
                self._SampleContainer__data = data

        class O(object):
            activated = False
            def __init__(self):
                self._p_jar = self
                self.current = []
                self.readCurrent = self.current.append

            def _p_activate(self):
                self.activated = True

        o = O()
        container = Base(o)
        readCurrent(container)
        assert_that(o, has_property('activated', True))
        assert_that(o, has_property('current', [o]))

class TestIsBroken(unittest.TestCase):

    def test_isBroken_no_obj(self):
        assert_that(isBroken(None, None), is_false())
        # WTF
        assert_that(isBroken(None, 'foo'), is_true())

    def test_isBroken_no_activate(self):
        class O(object):
            pass

        o = O()
        assert_that(isBroken(o), is_false())

        interface.alsoProvides(o, IBroken)
        assert_that(isBroken(o), is_true())

    def test_activate_errors(self):
        from ZODB.POSException import POSKeyError
        class O(object):
            raises = TypeError

            def _p_activate(self):
                raise self.raises()

        o = O()

        # Raising a TypeError doesn't do anything
        assert_that(isBroken(o), is_false())

        # POSKeyError does
        o.raises = POSKeyError
        assert_that(isBroken(o), is_true())


        # other exceptions are passed
        o.raises = KeyError
        self.assertRaises(KeyError, isBroken, o)

class TestBWCImports(unittest.TestCase):

    def test_urlproperty(self):
        import nti.zodb.urlproperty
        assert_that(nti.zodb.urlproperty, has_property('UrlProperty'))

    def test_schema(self):
        import nti.zodb.schema
        assert_that(nti.zodb.schema, has_property('Number'))
