# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from collective.wfadaptations.testing import COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestInstall(unittest.TestCase):
    """Test installation of collective.wfadaptations into Plone."""

    layer = COLLECTIVE_WFADAPTATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.wfadaptations is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.wfadaptations'))

    def test_uninstall(self):
        """Test if collective.wfadaptations is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.wfadaptations'])
        self.assertFalse(self.installer.isProductInstalled('collective.wfadaptations'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveWfadaptationsLayer is registered."""
        from collective.wfadaptations.interfaces import ICollectiveWfadaptationsLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveWfadaptationsLayer, utils.registered_layers())
