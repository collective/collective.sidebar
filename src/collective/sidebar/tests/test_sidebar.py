# -*- coding: utf-8 -*-

from collective.sidebar.browser.sidebar import get_action_icon
from collective.sidebar.browser.sidebar import SidebarViewlet
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
        self.nav_data_view = api.content.get_view(
            name='navData',
            context=self.portal,
            request=self.request,
        )
        self.viewlet = self.nav_data_view.render_viewlet

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
        self.assertIn('<a class="sidebar-back" href="http://nohost/plone">', self.viewlet(context=demo, request=self.request))   # noqa

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
        item1 = api.content.create(
            type='Document',
            container=self.portal,
            id='item1',
            title=u'Item1',
            description=u'',
        )
        self._check_in_private_state(item1)
        api.content.transition(obj=self.portal['item1'], transition='publish')
        self._check_in_published_state(item1)
        api.content.transition(obj=item1, transition='retract')
        api.content.transition(obj=self.portal['item1'], transition='submit')
        self._check_in_pending_state(item1)
        api.content.transition(obj=item1, transition='retract')
        self._check_in_private_state(item1)
        api.content.transition(obj=item1, transition='submit')
        api.content.transition(obj=item1, transition='publish')
        api.content.transition(obj=item1, transition='reject')
        self._check_in_private_state(item1)
        api.content.transition(obj=item1, transition='publish')
        self._check_in_published_state(item1)

    def _check_in_published_state(self, item1):
        self.assertEqual(api.content.get_state(item1), 'published')
        v = self.viewlet(context=item1, request=self.request)
        self.assertIn('<span class="menu-item-icon glyphicon glyphicon-record state-published', v)  # noqa
        self.assertIn('<span class="menu-item-title state-published', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=publish', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=submit', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=reject', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=retract', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_history', v)  # noqa

    def _check_in_pending_state(self, item1):
        self.assertEqual(api.content.get_state(item1), 'pending')
        v = self.viewlet(context=item1, request=self.request)
        self.assertIn('<span class="menu-item-icon glyphicon glyphicon-record state-pending', v)  # noqa
        self.assertIn('<span class="menu-item-title state-pending', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=publish', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=submit', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=reject', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=retract', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_history', v)  # noqa

    def _check_in_private_state(self, item1):
        self.assertEqual(api.content.get_state(item1), 'private')
        v = self.viewlet(context=item1, request=self.request)
        self.assertIn('<span class="menu-item-icon glyphicon glyphicon-record state-private', v)  # noqa
        self.assertIn('<span class="menu-item-title state-private', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=publish', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=submit', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=reject', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/item1/content_status_modify?workflow_action=retract', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/item1/content_status_history', v)  # noqa

    def test_workflow_colors(self):
        view = SidebarViewlet(self.portal, self.request, None, None)
        self.assertEqual(view.has_workflow_state_color(), 'with-state-color')

    def test_sections_collapse(self):
        api.portal.set_registry_record('collective.sidebar.enable_cookies', True)  # noqa
        api.portal.set_registry_record('collective.sidebar.enable_collapse', True)  # noqa
        v = self.viewlet(context=self.portal, request=self.request)
        self.assertNotIn('menu-section collapsed', v)  # noqa
        self.assertIn('<div id="sidebar-section-site" class="menu-section">', v)  # noqa
        self.request.set('sections', 'sidebar-section-site')
        v = self.viewlet(context=self.portal, request=self.request)
        self.assertIn('<div id="sidebar-section-site" class="menu-section collapsed">', v)  # noqa

    def test_actions(self):
        demo = api.content.create(
            type='Folder',
            container=self.portal,
            id='demo',
            title=u'Demo',
            description=u'Test',
        )
        v = self.viewlet(context=demo, request=self.request)
        self.assertIn('<a href="http://nohost/plone/demo/object_cut?_authenticator=', v)  # noqa
        # These are added in testing/actions.xml:
        self.assertIn('glyphicon-test', v)
        self.assertIn('glyphicon-star', v)
        self.assertIn('Test-Action', v)
        self.assertIn('No-Url-Action', v)
        self.assertIn('No-Icon-Action', v)

    def test_addable_items(self):
        # Test what can be added to normal folder
        demo = api.content.create(
            type='Folder',
            container=self.portal,
            id='demo',
            title=u'Demo',
            description=u'Test',
        )
        v = self.viewlet(context=demo, request=self.request)
        self.assertIn('<a href="http://nohost/plone/demo/++add++Image', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/demo/++add++File', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/demo/++add++Collection', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/demo/++add++News Item', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/demo/++add++Folder', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/demo/++add++Document', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/demo/++add++Event', v)  # noqa

        # Restrict what can be added to a folder and test it
        folder_fti = self.portal.portal_types['Folder']
        folder_fti.manage_changeProperties(
            filter_content_types=True, allowed_content_types=[])
        v = self.viewlet(context=demo, request=self.request)
        self.assertNotIn('<a href="http://nohost/plone/demo/++add++Image', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/demo/++add++File', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/demo/++add++Collection', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/demo/++add++News Item', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/demo/++add++Folder', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/demo/++add++Document', v)  # noqa
        self.assertNotIn('<a href="http://nohost/plone/demo/++add++Event', v)  # noqa
        self.assertNotIn('sidebar-section-add', v)

    def test_default_page_and_view_link(self):
        demo = api.content.create(
            type='Folder',
            container=self.portal,
            id='demo',
            title=u'Demo',
            description=u'Test',
        )
        demo2 = api.content.create(
            type='Folder',
            container=self.portal,
            id='demo2',
            title=u'Demo2',
            description=u'Test',
        )
        self.portal.setDefaultPage('demo')
        v = self.viewlet(context=self.portal, request=self.request)
        self.assertIn('<a href="http://nohost/plone/select_default_view" class="pat-plone-modal">', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/select_default_page" class="pat-plone-modal">', v)  # noqa
        v = self.viewlet(context=demo, request=self.request)
        self.assertIn('<a href="http://nohost/plone/select_default_view" class="pat-plone-modal">', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/select_default_page" class="pat-plone-modal">', v)  # noqa
        v = self.viewlet(context=demo2, request=self.request)
        self.assertIn('<a href="http://nohost/plone/demo2/select_default_view" class="pat-plone-modal">', v)  # noqa
        self.assertIn('<a href="http://nohost/plone/demo2/select_default_page" class="pat-plone-modal">', v)  # noqa

    def test_action_icon_map(self):
        self.assertEqual(get_action_icon('cut'), 'glyphicon glyphicon-scissors')  # noqa
        self.assertEqual(get_action_icon('copy'), 'glyphicon glyphicon-duplicate')  # noqa
        self.assertEqual(get_action_icon('paste'), 'glyphicon glyphicon-open-file')  # noqa
        self.assertEqual(get_action_icon('delete'), 'glyphicon glyphicon-trash')  # noqa
        self.assertEqual(get_action_icon('rename'), 'glyphicon glyphicon-random')  # noqa
        self.assertEqual(get_action_icon('ical_import_enable'), 'glyphicon glyphicon-calendar')  # noqa
        self.assertEqual(get_action_icon('ical_import_disable'), 'glyphicon glyphicon-calendar')  # noqa
        self.assertEqual(get_action_icon('not-defined'), 'glyphicon glyphicon-star')  # noqa
        self.assertEqual(get_action_icon(None), 'glyphicon glyphicon-star')  # noqa
        self.assertEqual(get_action_icon(-15), 'glyphicon glyphicon-star')  # noqa
        self.assertEqual(get_action_icon(True), 'glyphicon glyphicon-star')  # noqa
        self.assertEqual(get_action_icon(False), 'glyphicon glyphicon-star')  # noqa

    def test_sidebar_ajax(self):
        self.assertIsNone(self.nav_data_view(None))
        self.assertIsNotNone(self.nav_data_view(render=True))
