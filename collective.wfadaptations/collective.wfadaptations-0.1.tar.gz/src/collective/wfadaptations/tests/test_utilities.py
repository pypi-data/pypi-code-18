# -*- coding: utf-8 -*-
"""Test utility."""
import unittest2 as unittest

from zope.component import getGlobalSiteManager, getUtility

from collective.wfadaptations.interfaces import IWorkflowAdaptation
from collective.wfadaptations.tests.base import DummyWorkflowAdaptation
from collective.wfadaptations.testing import COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING  # noqa


class TestUtility(unittest.TestCase):

    """Test workflow adaptation utility."""

    layer = COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING

    def test_register_utility(self):
        gsm = getGlobalSiteManager()
        my_wf_adaptation = DummyWorkflowAdaptation()
        gsm.registerUtility(
            my_wf_adaptation,
            IWorkflowAdaptation,
            'my_wf_adaptation')
        utility = getUtility(IWorkflowAdaptation, 'my_wf_adaptation')
        self.assertEqual(my_wf_adaptation, utility)
        gsm.unregisterUtility(utility, IWorkflowAdaptation, 'my_wf_adaptation')
