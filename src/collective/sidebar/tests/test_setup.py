# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.sidebar.interfaces import ICollectiveSidebarLayer
from collective.sidebar.testing import COLLECTIVE_SIDEBAR_INTEGRATION_TESTING  # noqa
from plone.browserlayer import utils
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.sidebar is properly installed."""

    layer = COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if plonetheme.siguv is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'collective.sidebar'))

    def test_browserlayer(self):
        """Test that ICollectiveSidebarLayer is registered."""
        self.assertIn(ICollectiveSidebarLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if plonetheme.siguv is installed."""
        self.assertTrue(
            self.installer.is_product_installed('collective.sidebar'))

    def test_browserlayer(self):
        """Test that ICollectiveSidebarLayer is registered."""
        self.assertIn(ICollectiveSidebarLayer, utils.registered_layers())

    def test_product_uninstalled(self):
        """Test if plonetheme.siguv is cleanly uninstalled."""
        self.assertTrue(
            self.installer.is_product_installed('collective.sidebar'))
        self.installer.uninstall_product('collective.sidebar')
        self.assertFalse(
            self.installer.is_product_installed('collective.sidebar'))

    def test_browserlayer_removed(self):
        """Test that IPlonethemeSiguvLayer is removed."""
        self.assertTrue(
            self.installer.is_product_installed('collective.sidebar'))
        self.installer.uninstall_product('collective.sidebar')
        self.assertNotIn(ICollectiveSidebarLayer, utils.registered_layers())
