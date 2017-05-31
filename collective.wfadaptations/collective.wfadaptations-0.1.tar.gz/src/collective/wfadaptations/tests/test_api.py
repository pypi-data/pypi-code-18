# -*- coding: utf-8 -*-
"""Test api."""
import unittest2 as unittest

from zope.component import getGlobalSiteManager, getUtility

from plone import api

from collective.wfadaptations.interfaces import IWorkflowAdaptation
from collective.wfadaptations.tests.base import DummyWorkflowAdaptation
from collective.wfadaptations.api import get_applied_adaptations
from collective.wfadaptations.api import add_applied_adaptation
from collective.wfadaptations.api import get_applied_adaptations_by_workflows
from collective.wfadaptations.api import get_applied_adaptations_for_workflow
from collective.wfadaptations.api import apply_from_registry
from collective.wfadaptations.api import AdaptationAlreadyAppliedException
from collective.wfadaptations.testing import COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING  # noqa


RECORD_NAME = 'collective.wfadaptations.applied_adaptations'


class TestAPI(unittest.TestCase):

    """Test API."""

    layer = COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING

    def setUp(self):
        applied_adaptations = [
            {u'workflow': u'workflow1',
             u'adaptation': u'adaptation1',
             u'parameters': u'{}'
            },
            {u'workflow': u'workflow1',
             u'adaptation': u'adaptation2',
             u'parameters': u'{}'
            },
            {u'workflow': u'workflow2',
             u'adaptation': u'adaptation2',
             u'parameters': u'{"param": "foobar"}'
            },
        ]
        api.portal.set_registry_record(
            RECORD_NAME, applied_adaptations)

        gsm = getGlobalSiteManager()
        self.dummy_wf_adaptation = DummyWorkflowAdaptation()
        gsm.registerUtility(
            self.dummy_wf_adaptation,
            IWorkflowAdaptation,
            'dummy_adaptation')

    def tearDown(self):
        gsm = getGlobalSiteManager()
        utility = getUtility(IWorkflowAdaptation, 'dummy_adaptation')
        gsm.unregisterUtility(utility, IWorkflowAdaptation, 'dummy_adaptation')

    def test_get_applied_adaptations(self):
        applied_adaptations = get_applied_adaptations()
        self.assertIn(
            {u'workflow': u'workflow1',
             u'adaptation': u'adaptation1',
             u'parameters': {}
            },
            applied_adaptations,
            )

        self.assertIn(
            {u'workflow': u'workflow1',
             u'adaptation': u'adaptation2',
             u'parameters': {}
            },
            applied_adaptations,
            )

        self.assertIn(
            {u'workflow': u'workflow2',
             u'adaptation': u'adaptation2',
             u'parameters': {u"param": u"foobar"}
            },
            applied_adaptations,
            )

    def test_add_applied_adaptation(self):
        params = {'param1': 'foo', 'param2': 'bar'}
        add_applied_adaptation(u'adaptation1', u'workflow2', **params)
        self.assertIn(
            {u'workflow': u'workflow2',
             u'adaptation': u'adaptation1',
             u'parameters': u'{"param1": "foo", "param2": "bar"}'
            },
            api.portal.get_registry_record(RECORD_NAME),
            )
        with self.assertRaises(AdaptationAlreadyAppliedException):
            add_applied_adaptation(u'adaptation1', u'workflow1', **params)

    def test_get_applied_adaptations_by_workflow(self):
        expected = {
            u'workflow1': [u'adaptation1', u'adaptation2'],
            u'workflow2': [u'adaptation2']
            }
        self.assertEqual(expected, get_applied_adaptations_by_workflows())

    def test_get_applied_adaptations_for_workflow(self):
        expected = [u'adaptation1', u'adaptation2']
        self.assertEqual(
            expected,
            get_applied_adaptations_for_workflow('workflow1'))
        self.assertEqual(
            [],
            get_applied_adaptations_for_workflow('workflow3'))

    def test_apply_from_registry(self):
        success, errors = apply_from_registry()
        self.assertEqual(success, 0)
        self.assertEqual(errors, 3)

        # empty registry, add a real adaptation and try again
        api.portal.set_registry_record(
            RECORD_NAME,
            [{u'adaptation': u'dummy_adaptation',
              u'workflow': u'intranet_workflow',
              u'parameters': u'{"param": "foobar"}'
             }])
        success, errors = apply_from_registry()
        self.assertEqual(success, 1)
        self.assertEqual(errors, 0)
        # test that the patch has been applied
        self.assertEqual(
            self.dummy_wf_adaptation.patched, 'intranet_workflow;foobar')
