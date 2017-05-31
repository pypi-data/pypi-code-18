# -*- coding: utf-8 -*-

import unittest

from plone import api

from collective.behavior.internalnumber.testing import COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING  # noqa

from .. import TYPE_CONFIG
from ..browser.settings import get_pt_settings
from ..subscribers import object_added


class TestSubscribers(unittest.TestCase):
    """Test settings."""

    layer = COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.tt1 = self.portal['tt1']
        api.portal.set_registry_record(TYPE_CONFIG, [{u'portal_type': u'glo_bal', u'uniqueness': False,
                                                      u'default_number': 1, u'default_expression': u'number'},
                                                     {u'portal_type': u'testtype', u'uniqueness': True,
                                                      u'default_number': 1, u'default_expression': u'number'}])

    def test_object_added(self):
        self.assertDictEqual(get_pt_settings(u'testtype'), {u'u': True, u'nb': 1, 'expr': u'number'})
        self.assertDictEqual(get_pt_settings(u'glo_bal'), {u'u': False, u'nb': 1, 'expr': u'number'})
        # test with testtype
        object_added(self.tt1, None)
        self.assertDictEqual(get_pt_settings(u'testtype'), {u'u': True, u'nb': 2, 'expr': u'number'})
        self.assertDictEqual(get_pt_settings(u'glo_bal'), {u'u': False, u'nb': 1, 'expr': u'number'})

        class Dummy(object):
            def __init__(self, val=None, pt='unknown'):
                self.internal_number = val
                self.portal_type = pt
        # test with other type
        object_added(Dummy(val='xxx'), None)
        self.assertDictEqual(get_pt_settings(u'testtype'), {u'u': True, u'nb': 2, 'expr': u'number'})
        self.assertDictEqual(get_pt_settings(u'glo_bal'), {u'u': False, u'nb': 2, 'expr': u'number'})
        # test with empty value
        object_added(Dummy(), None)
        self.assertDictEqual(get_pt_settings(u'testtype'), {u'u': True, u'nb': 2, 'expr': u'number'})
        self.assertDictEqual(get_pt_settings(u'glo_bal'), {u'u': False, u'nb': 2, 'expr': u'number'})
        # test with empty config
        api.portal.set_registry_record(TYPE_CONFIG, [])
        object_added(Dummy(self.tt1), None)
        self.assertDictEqual(get_pt_settings(u'testtype'), {})
        self.assertDictEqual(get_pt_settings(u'glo_bal'), {})
