# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from zope.schema._bootstrapinterfaces import WrongType

from collective.behavior.internalnumber.testing import COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING  # noqa
from plone import api

from .. import TYPE_CONFIG


class TestSetup(unittest.TestCase):
    """Test that collective.behavior.internalnumber is properly installed."""

    layer = COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.behavior.internalnumber is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.behavior.internalnumber'))

    def test_browserlayer(self):
        """Test that ICollectiveBehaviorInternalnumberLayer is registered."""
        from collective.behavior.internalnumber.interfaces import (
            ICollectiveBehaviorInternalnumberLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveBehaviorInternalnumberLayer, utils.registered_layers())

    def test_registry(self):
        self.assertRaises(api.exc.InvalidParameterError, api.portal.set_registry_record, 'Unexistent key', True)
        self.assertRaises(WrongType, api.portal.set_registry_record, TYPE_CONFIG, 'string')
        api.portal.set_registry_record(TYPE_CONFIG, [])


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.behavior.internalnumber'])

    def test_product_uninstalled(self):
        """Test if collective.behavior.internalnumber is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.behavior.internalnumber'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveBehaviorInternalnumberLayer is removed."""
        from collective.behavior.internalnumber.interfaces import ICollectiveBehaviorInternalnumberLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveBehaviorInternalnumberLayer, utils.registered_layers())
