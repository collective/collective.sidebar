# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.sidebar.testing import COLLECTIVE_SIDEBAR_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.sidebar is properly installed."""

    layer = COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.sidebar is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.sidebar'))

    def test_browserlayer(self):
        """Test that ICollectiveSidebarLayer is registered."""
        from collective.sidebar.interfaces import (
            ICollectiveSidebarLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveSidebarLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.sidebar'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.sidebar is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.sidebar'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveSidebarLayer is removed."""
        from collective.sidebar.interfaces import \
            ICollectiveSidebarLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveSidebarLayer,
            utils.registered_layers())
