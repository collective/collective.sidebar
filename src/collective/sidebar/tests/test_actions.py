# -*- coding: utf-8 -*-

from collective.sidebar.testing import COLLECTIVE_SIDEBAR_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME

import unittest


class TestActionsFunctional(unittest.TestCase):

    layer = COLLECTIVE_SIDEBAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.nav_data_view = api.content.get_view(
            name='navData',
            context=self.portal,
            request=self.request,
        )
        self.viewlet = self.nav_data_view.render_viewlet
        self.portal_actions = api.portal.get_tool('portal_actions')
        self.sidebar_links = self.portal_actions.get('sidebar_links')
        login(self.portal, SITE_OWNER_NAME)

    def test_action_links(self):
        # Logout action only visible to authenticated users
        self.assertIn(
            '<span class="menu-item-title">Logout</span>',
            self.viewlet(context=self.portal, request=self.request),
        )
        # Visibility should be respected
        home_el = '<span class="menu-item-title">Home</span>'
        self.assertIn(
            home_el,
            self.viewlet(context=self.portal, request=self.request),
        )
        home_link = self.sidebar_links.get('home')
        home_link.visible = False
        self.assertNotIn(
            home_el,
            self.viewlet(context=self.portal, request=self.request),
        )
        # Add a new action to the sidebar_links
        new_action_view = api.content.get_view(
            name='new-action',
            context=self.portal,
            request=self.request,
        )
        new_action_view.createAndAdd({
            'id': 'Contact',
            'category': 'sidebar_links',
        })
        self.assertIn(
            '<span class="menu-item-title">Contact</span>',
            self.viewlet(context=self.portal, request=self.request),
        )
