# -*- coding: utf-8 -*-

from collective.sidebar.testing import COLLECTIVE_SIDEBAR_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import SITE_OWNER_NAME

import unittest


class TestSidebarFunctional(unittest.TestCase):

    layer = COLLECTIVE_SIDEBAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        login(self.portal, SITE_OWNER_NAME)

    def test_profile_section(self):
        nav_data_view = api.content.get_view(
            name='navData',
            context=self.portal,
            request=self.request,
        )
        viewlet = nav_data_view.render_viewlet
        viewlet(context=self.portal, request=self.request)
        self.assertIn(
            '<div class="profile-name">admin</div>',
            viewlet(context=self.portal, request=self.request),
        )
        # Login with user that has fullname property set
        logout()
        login(self.portal, 'mmustermann')
        self.assertIn(
            '<div class="profile-name">Max Mustermann</div>',
            viewlet(context=self.portal, request=self.request),
        )

    def test_link_section(self):
        nav_data_view = api.content.get_view(
            name='navData',
            context=self.portal,
            request=self.request,
        )
        viewlet = nav_data_view.render_viewlet
        viewlet(context=self.portal, request=self.request)
        self.assertIn(
            '<div id="sidebar-section-links" class="menu-section">',
            viewlet(context=self.portal, request=self.request),
        )
        # Login with user that has fullname property set
        ac = self.portal.portal_actions.sidebar_links
        ac['home'].visible = False
        ac['login'].visible = False
        ac['logout'].visible = False
        self.assertNotIn(
            '<div id="sidebar-section-links" class="menu-section">',
            viewlet(context=self.portal, request=self.request),
        )
        logout()
