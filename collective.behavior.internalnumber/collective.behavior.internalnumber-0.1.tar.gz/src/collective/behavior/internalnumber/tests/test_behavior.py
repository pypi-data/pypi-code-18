# -*- coding: utf-8 -*-

import unittest

from zope.component import getUtility
from zope.interface import Invalid

from plone import api
from plone.dexterity.interfaces import IDexterityFTI

from collective.behavior.internalnumber.testing import COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING  # noqa

from .. import TYPE_CONFIG
from ..behavior import validateIndexValueUniqueness, InternalNumberValidator, internal_number_default


class TestBehavior(unittest.TestCase):
    """Test behavior."""

    layer = COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.tt1 = self.portal['tt1']
        self.tt2 = api.content.create(container=self.portal, id='tt2', type='testtype', title='Another title')
        self.tt2.reindexObject()
        api.portal.set_registry_record(TYPE_CONFIG, [{u'portal_type': u'testtype', u'uniqueness': True,
                                                      u'default_number': 1, u'default_expression': u'number'}])

    def test_content(self):
        self.assertEqual(self.tt1.internal_number, 'AA123')
        self.assertEqual(self.tt2.internal_number, None)

    def test_index(self):
        pc = self.portal.portal_catalog
        brains = pc(portal_type='testtype')
        self.assertEqual(len(brains), 2)
        brains = pc(portal_type='testtype', internal_number='AA123')
        self.assertEqual(len(brains), 1)

    def test_searchabletext_index(self):
        fti = getUtility(IDexterityFTI, name='testtype')
        behaviors = list(fti.behaviors)
        behaviors.append('collective.dexteritytextindexer.behavior.IDexterityTextIndexer')
        fti._updateProperty('behaviors', tuple(behaviors))
        self.tt1.reindexObject()
        pc = self.portal.portal_catalog
        brains = pc(portal_type='testtype', SearchableText='AA123')
        self.assertEqual(len(brains), 1)
        self.assertEqual(brains[0].getObject(), self.tt1)
        brains = pc(portal_type='testtype', SearchableText='content')
        self.assertEqual(len(brains), 1)
        self.assertEqual(brains[0].getObject(), self.tt1)

    def test_validator(self):
        self.assertRaises(Invalid, validateIndexValueUniqueness, self.tt2, 'testtype', 'internal_number', 'AA123')
        self.assertIsNone(validateIndexValueUniqueness(self.tt2, 'testtype', 'internal_number', 'AA1234'))
        # context, request, view, field, widget
        # make validator with tt2 as context and tt2 as portal_type
        validator = InternalNumberValidator(self.tt2, None, self.tt2, None, None)
        # validate following configuration: flag is True
        self.assertRaises(Invalid, validator.validate, 'AA123')
        self.assertIsNone(validator.validate('AA1234'))
        # validate following configuration: flag is not defined
        api.portal.set_registry_record(TYPE_CONFIG, [])
        self.assertRaises(Invalid, validator.validate, 'AA123')
        self.assertIsNone(validator.validate('AA1234'))
        # validate following configuration: flag is globally defined
        api.portal.set_registry_record(TYPE_CONFIG, [{u'portal_type': u'glo_bal', u'uniqueness': False,
                                                      u'default_number': 1, u'default_expression': u'number'}])
        self.assertIsNone(validator.validate('AA123'))
        # validate following configuration: flag is False
        api.portal.set_registry_record(TYPE_CONFIG, [{u'portal_type': u'testtype', u'uniqueness': False,
                                                      u'default_number': 1, u'default_expression': u'number'}])
        self.assertIsNone(validator.validate('AA123'))
        # make validator with portal as context and tt2 as portal_type
        validator = InternalNumberValidator(self.portal, None, self.tt2, None, None)
        api.portal.set_registry_record(TYPE_CONFIG, [])
        self.assertRaises(Invalid, validator.validate, 'AA123')
        self.assertIsNone(validator.validate('AA1234'))

    def test_internal_number_default(self):
        class Dummy(object):
            def __init__(self, obj):
                self.context = obj
                self.portal_type = obj.portal_type
                self.view = None
        dummy1 = Dummy(self.tt1)
        dummy1.view = dummy1
        self.assertEqual(internal_number_default(dummy1), 1)
        api.portal.set_registry_record(TYPE_CONFIG, [{u'portal_type': u'testtype', u'uniqueness': False,
                                                      u'default_number': 1,
                                                      u'default_expression': u"python: 'Num: %d' % (number+1)"}])
        self.assertEqual(internal_number_default(dummy1), 'Num: 2')
