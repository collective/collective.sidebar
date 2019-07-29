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

    def test_back_button(self):
        # Go to portal_root -> no back button
        # Go to empty folder -> back button
        # Go to filled folder -> back button
        # Go to item in folder -> back button
        # Go to LRF Item -> no back button
        # Go to default page on front page -> no back button
        # Try to throw the AttributeError
        pass

    def test_content_can_be_added(self):
        # is _contentCanBeAdded still used?
        pass

    def test_get_search_path(self):
        # query-parameter can be removed from the function or needs testing
        pass

    def test_check_item(self):
        # Normal folder -> folder should be shown
        # Normal item -> parent should be shown
        # Exclude item from nav -> should not be shown
        # default-page -> should not be shown?
        pass

    def test_root_nav(self):
        # Enable root_nav -> always show root level nav -> Test in folder! and item in folder!  # noqa
        pass

    def test_get_items(self):
        # There is a try-except -> Try to run into Exception!
        # Create tree of folder1 -> item1+item2+folder2->item3
        # Check that each item in the tree shows correct nav items
        pass

    def test_workflows(self):
        # Click through states and check state titles and urls (unpublished, review, not passing review, published,...)  # noqa
        pass

    def test_workflow_colors(self):
        # Use it or remove it
        pass

    def test_sections_collapse(self):
        # collapse sections
        pass

    def test_actions(self):
        # Test actions with icons set and not set
        # Test actions with url set and not set
        # move this test to test_actions.py
        pass

    def test_addable_items(self):
        # Test what can be added to normal folder
        # Restrict what can be added to a folder and test it!
        pass

    def test_default_page_and_view_link(self):
        # test default view link and default page link
        # on default-pages and non-default pages
        pass

    def test_action_icon_map(self):
        # Test that the map is filled and else-case
        pass

    def test_sidebar_ajax(self):
        # according to coverage __call__ is never called???
        pass
