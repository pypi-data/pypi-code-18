# -*- coding: utf-8 -*-
"""Test vocabularies."""
from zope.component import getGlobalSiteManager, getUtility
from zope.schema.interfaces import IVocabularyFactory

from plone import api

import unittest2 as unittest

from collective.wfadaptations.interfaces import IWorkflowAdaptation
from collective.wfadaptations.testing import COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING  # noqa
from collective.wfadaptations.tests.base import DummyWorkflowAdaptation, \
    AnotherWorkflowAdaptation


class TestVocabularies(unittest.TestCase):

    """Test vocabularies."""

    layer = COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = api.portal.get()
        gsm = getGlobalSiteManager()
        my_wf_adaptation = DummyWorkflowAdaptation()
        my_other_wf_adaptation = DummyWorkflowAdaptation()
        another_wf_adaptation = AnotherWorkflowAdaptation()
        self.utilities = {
            'my_wf_adaptation': my_wf_adaptation,
            'my_other_wf_adaptation': my_other_wf_adaptation,
            'another_wf_adaptation': another_wf_adaptation,
        }
        for name, adaptation in self.utilities.iteritems():
            gsm.registerUtility(adaptation, IWorkflowAdaptation, name)

    def tearDown(self):
        gsm = getGlobalSiteManager()
        for name in self.utilities.keys():
            utility = getUtility(IWorkflowAdaptation, name)
            gsm.unregisterUtility(utility, IWorkflowAdaptation, name)

    def test_wfadaptations_vocabulary(self):
        vocabulary_factory = getUtility(
            IVocabularyFactory,
            name="collective.wfadaptations.WorkflowAdaptations")
        vocabulary = vocabulary_factory(self.portal)
        self.assertEqual(4, len(vocabulary))
        tokens = [term.token for term in vocabulary]
        self.assertIn('collective.wfadaptations.example', tokens)
        self.assertIn('my_wf_adaptation', tokens)
        self.assertIn('my_other_wf_adaptation', tokens)
        self.assertIn('another_wf_adaptation', tokens)
