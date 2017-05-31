# -*- coding: utf-8 -*-
"""Test associate views."""
import unittest2 as unittest

from zope.component import getGlobalSiteManager, getUtility

from plone.app.testing.interfaces import TEST_USER_NAME

from ecreall.helpers.testing.base import BaseTest

from collective.wfadaptations.api import get_applied_adaptations
from collective.wfadaptations.interfaces import IWorkflowAdaptation
from collective.wfadaptations.tests.base import DummyWorkflowAdaptation
from collective.wfadaptations.testing import COLLECTIVE_WFADAPTATIONS_FUNCTIONAL_TESTING  # noqa


class TestParametersForm(unittest.TestCase, BaseTest):

    """Test workflow adaptation utility."""

    layer = COLLECTIVE_WFADAPTATIONS_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestParametersForm, self).setUp()
        self.portal = self.layer['portal']
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

    def simulate_form_submit(self, request):
        """Simulate form submit."""
        view = self.portal.restrictedTraverse('associate_workflow_adaptation')
        view.request = request
        view()
        form = view.form(self.portal, request)
        form.update()
        view.form.handleApply(form, None)

    def test_parameters_form(self):
        self.login(TEST_USER_NAME)
        request = self.portal.REQUEST
        request.form['form.widgets.workflow'] = ['intranet_workflow']
        request.form['form.widgets.adaptation'] = ['dummy_adaptation']
        request.form['form.widgets.param'] = 'foobar'
        self.simulate_form_submit(request)

        # test that the patch has been applied
        self.assertEqual(
            self.dummy_wf_adaptation.patched, 'intranet_workflow;foobar')

        # test that the record has been updated
        self.assertIn(
            {'adaptation': 'dummy_adaptation',
             'workflow': 'intranet_workflow',
             'parameters': {"param": "foobar"}
            },
            get_applied_adaptations(),
            )
