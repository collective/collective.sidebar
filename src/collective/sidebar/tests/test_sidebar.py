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
        nav_data_view = api.content.get_view(
            name='navData',
            context=self.portal,
            request=self.request,
        )
        self.viewlet = nav_data_view.render_viewlet

    def test_profile_section(self):
        self.viewlet(context=self.portal, request=self.request)
        self.assertIn(
            '<div class="profile-name">admin</div>',
            self.viewlet(context=self.portal, request=self.request),
        )
        # Login with user that has fullname property set
        logout()
        login(self.portal, 'mmustermann')
        self.assertIn(
            '<div class="profile-name">Max Mustermann</div>',
            self.viewlet(context=self.portal, request=self.request),
        )

    def test_link_section(self):
        self.assertIn(
            '<div id="sidebar-section-links" class="menu-section">',
            self.viewlet(context=self.portal, request=self.request),
        )
        # Login with user that has fullname property set
        ac = self.portal.portal_actions.sidebar_links
        ac['home'].visible = False
        ac['login'].visible = False
        ac['logout'].visible = False
        self.assertNotIn(
            '<div id="sidebar-section-links" class="menu-section">',
            self.viewlet(context=self.portal, request=self.request),
        )
        logout()

    def test_back_button(self):
        # Go to portal_root -> no back button
        self.assertNotIn('<a class="sidebar-back"', self.viewlet(context=self.portal, request=self.request))  # noqa

        # Go to empty folder -> back button
        demo = api.content.create(
            type='Folder',
            container=self.portal,
            id='demo',
            title=u'Demo',
            description=u'Test',
        )
        # MR is up to fix this
        #self.assertIn('<a class="sidebar-back" href="http://nohost/plone">', viewlet(context=demo, request=self.request))   # noqa

        # Go to filled folder -> back button
        link = api.content.create(
            type='Link',
            container=demo,
            id='test',
            title=u'Test',
            remoteUrl='${portal_url}/test_rendering',
        )
        self.assertIn('<a class="sidebar-back" href="http://nohost/plone"', self.viewlet(context=demo, request=self.request))  # noqa

        # Go to item in folder -> back button
        self.assertIn('<a class="sidebar-back" href="http://nohost/plone/demo"', self.viewlet(context=link, request=self.request))  # noqa

        # Go to default page on front page -> no back button
        page = api.content.create(
            type='Document',
            container=self.portal,
            id='test-page',
            title=u'Test Page',
        )
        self.portal.setDefaultPage('test-page')
        self.assertNotIn('<a class="sidebar-back"', self.viewlet(context=page, request=self.request))  # noqa

        # Go to default page on folder -> back button
        page2 = api.content.create(
            type='Document',
            container=demo,
            id='test-page2',
            title=u'Test Page2',
        )
        demo.setDefaultPage('test-page2')
        self.assertIn('<a class="sidebar-back" href="http://nohost/plone">', self.viewlet(context=page2, request=self.request))  # noqa

    def test_content_can_be_added(self):
        demo = api.content.create(
            type='Folder',
            container=self.portal,
            id='demo',
            title=u'Demo',
            description=u'Test',
        )
        self.portal.setDefaultPage('demo')
        self.assertIn('<a href="http://nohost/plone/demo/@@folder_factories">', self.viewlet(context=demo, request=self.request))  # noqa

    def test_check_item(self):
        # Normal folder -> folder should be shown
        # Normal item -> parent should be shown
        demo = api.content.create(
            type='Folder',
            container=self.portal,
            id='demo',
            title=u'Demo',
            description=u'Test',
        )
        self.assertIn('<span class="menu-item-title">Demo</span>', self.viewlet(context=self.portal, request=self.request))  # noqa
        pagey = api.content.create(
            type='Document',
            container=demo,
            id='pagey',
            title=u'Pagey',
        )
        self.assertIn('<span class="menu-item-title">Pagey</span>', self.viewlet(context=demo, request=self.request))  # noqa
        self.assertIn('<span class="menu-item-title">Pagey</span>', self.viewlet(context=pagey, request=self.request))  # noqa

        # Exclude item from nav -> should not be shown
        pagey.exclude_from_nav = True
        pagey.reindexObject()
        self.assertNotIn('<span class="menu-item-title">Pagey</span>', self.viewlet(context=demo, request=self.request))  # noqa

        # default-page -> should not be shown?
        pagey.exclude_from_nav = False
        pagey.reindexObject()
        demo.setDefaultPage('pagey')
        self.assertNotIn('<span class="menu-item-title">Pagey</span>', self.viewlet(context=demo, request=self.request))  # noqa

    def test_root_nav(self):
        api.portal.set_registry_record(
            name='collective.sidebar.root_nav',
            value=True,
        )
        api.content.create(
            type='Folder',
            container=self.portal,
            id='testi',
            title=u'Testi',
            description=u'Testi im Root Level',
        )
        demo = api.content.create(
            type='Folder',
            container=self.portal,
            id='demo',
            title=u'Demo',
            description=u'Test',
        )
        pagey = api.content.create(
            type='Document',
            container=demo,
            id='pagey',
            title=u'Pagey',
        )
        self.assertIn('<span class="menu-item-title">Testi</span>', self.viewlet(context=self.portal, request=self.request))  # noqa
        self.assertIn('<span class="menu-item-title">Demo</span>', self.viewlet(context=self.portal, request=self.request))  # noqa
        self.assertNotIn('<span class="menu-item-title">Pagey</span>', self.viewlet(context=self.portal, request=self.request))  # noqa
        self.assertIn('<span class="menu-item-title">Testi</span>', self.viewlet(context=demo, request=self.request))  # noqa
        self.assertIn('<span class="menu-item-title">Demo</span>', self.viewlet(context=demo, request=self.request))  # noqa
        self.assertNotIn('<span class="menu-item-title">Pagey</span>', self.viewlet(context=demo, request=self.request))  # noqa
        self.assertIn('<span class="menu-item-title">Testi</span>', self.viewlet(context=pagey, request=self.request))  # noqa
        self.assertIn('<span class="menu-item-title">Demo</span>', self.viewlet(context=pagey, request=self.request))  # noqa
        self.assertNotIn('<span class="menu-item-title">Pagey</span>', self.viewlet(context=pagey, request=self.request))  # noqa

    def test_get_items(self):
        # Create tree of folder1 -> item1+item2+folder2->item3
        folder1 = api.content.create(
            type='Folder',
            container=self.portal,
            id='folder1',
            title=u'Folder1',
            description=u'',
        )
        item1 = api.content.create(
            type='Document',
            container=folder1,
            id='item1',
            title=u'Item1',
            description=u'',
        )
        item2 = api.content.create(
            type='Document',
            container=folder1,
            id='item2',
            title=u'Item2',
            description=u'',
        )
        folder2 = api.content.create(
            type='Folder',
            container=folder1,
            id='folder2',
            title=u'Folder2',
            description=u'',
        )
        item3 = api.content.create(
            type='Document',
            container=folder2,
            id='item3',
            title=u'Item3',
            description=u'',
        )

        v_portal = self.viewlet(context=self.portal, request=self.request)
        v_folder1 = self.viewlet(context=folder1, request=self.request)
        v_item1 = self.viewlet(context=item1, request=self.request)
        v_item2 = self.viewlet(context=item2, request=self.request)
        v_folder2 = self.viewlet(context=folder2, request=self.request)
        v_item3 = self.viewlet(context=item3, request=self.request)

        self.assertIn('<span class="menu-item-title">Folder1</span>', v_portal)  # noqa
        self.assertNotIn('<span class="menu-item-title">Folder2</span>', v_portal)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item1</span>', v_portal)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item2</span>', v_portal)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item3</span>', v_portal)  # noqa

        self.assertNotIn('<span class="menu-item-title">Folder1</span>', v_folder1)  # noqa
        self.assertIn('<span class="menu-item-title">Folder2</span>', v_folder1)  # noqa
        self.assertIn('<span class="menu-item-title">Item1</span>', v_folder1)  # noqa
        self.assertIn('<span class="menu-item-title">Item2</span>', v_folder1)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item3</span>', v_folder1)  # noqa

        self.assertNotIn('<span class="menu-item-title">Folder1</span>', v_item1)  # noqa
        self.assertIn('<span class="menu-item-title">Folder2</span>', v_item1)  # noqa
        self.assertIn('<span class="menu-item-title">Item1</span>', v_item1)  # noqa
        self.assertIn('<span class="menu-item-title">Item2</span>', v_item1)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item3</span>', v_item1)  # noqa

        self.assertNotIn('<span class="menu-item-title">Folder1</span>', v_item2)  # noqa
        self.assertIn('<span class="menu-item-title">Folder2</span>', v_item2)  # noqa
        self.assertIn('<span class="menu-item-title">Item1</span>', v_item2)  # noqa
        self.assertIn('<span class="menu-item-title">Item2</span>', v_item2)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item3</span>', v_item2)  # noqa

        self.assertNotIn('<span class="menu-item-title">Folder1</span>', v_folder2)  # noqa
        self.assertNotIn('<span class="menu-item-title">Folder2</span>', v_folder2)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item1</span>', v_folder2)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item2</span>', v_folder2)  # noqa
        self.assertIn('<span class="menu-item-title">Item3</span>', v_folder2)  # noqa

        self.assertNotIn('<span class="menu-item-title">Folder1</span>', v_item3)  # noqa
        self.assertNotIn('<span class="menu-item-title">Folder2</span>', v_item3)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item1</span>', v_item3)  # noqa
        self.assertNotIn('<span class="menu-item-title">Item2</span>', v_item3)  # noqa
        self.assertIn('<span class="menu-item-title">Item3</span>', v_item3)  # noqa

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
