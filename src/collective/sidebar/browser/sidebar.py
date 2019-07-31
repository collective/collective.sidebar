# -*- coding: utf-8 -*-

from collective.sidebar import _
from collective.sidebar.utils import crop
from collective.sidebar.utils import get_user
from plone import api
from plone.app.content.browser.folderfactories import _allowedTypes
from plone.app.layout.viewlets.common import ViewletBase
from plone.protect.utils import addTokenToUrl
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import IConstrainTypes
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter

import pkg_resources


class SidebarViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/sidebar.pt')

    def _contentCanBeAdded(self, addContext, request):
        """
        Find out if content can be added either by local constraints on the
        current context or by allowed_content_types on the FTI.
        """
        constrain = IConstrainTypes(addContext, None)
        if constrain is None:
            return _allowedTypes(request, addContext)
        return constrain.getLocallyAllowedTypes()

    def is_anonymous(self):
        """
        Check if the user is anonymous.
        """
        return api.user.is_anonymous()

    def get_portal_url(self):
        """
        Return the portal URL.
        """
        return api.portal.get().absolute_url()

    def get_static_links(self):
        """
        Return sidebar links from portal_actions.
        """
        cx = self.context
        filtered = cx.portal_actions.listFilteredActionsFor(cx)
        sidebar_links = filtered.get('sidebar_links', [])
        return sidebar_links

    def get_user_data(self):
        user = get_user()
        mtool = api.portal.get_tool('portal_membership')
        portrait = mtool.getPersonalPortrait(id=user[1])
        user_info = mtool.getMemberInfo(user[1])
        portal_url = self.get_portal_url()
        data = {
            'user_info': user_info,
            'portrait': portrait.absolute_url(),
            'user_url': portal_url + '/@@personal-information',
        }
        return data

    def get_search_path(self):
        """
        Return a search URL using the SearchableText attribute.
        """
        portal_url = self.get_portal_url()
        return '{0}/@@search?SearchableText='.format(portal_url)

    def get_navigation_root_url(self):
        """
        Return navigation root URL based on the language.
        """
        navigation_root = api.portal.get_navigation_root(self.context)
        return navigation_root.absolute_url()

    def get_back(self):
        """
        Get link to parent.
        """
        context = self.context
        portal = api.portal.get()
        parent = context.aq_parent
        root_nav = api.portal.get_registry_record(
            name='collective.sidebar.root_nav',
            default=False,
        )
        if context == portal or context.portal_type == 'LRF' or root_nav:
            return None
        try:
            if parent.default_page == context.id:
                if parent == api.portal.get_navigation_root(context):
                    return None
                return parent.aq_parent.absolute_url()
        except AttributeError:
            pass
        return parent.absolute_url()

    def can_edit(self):
        """
        Check if the user can modify content.
        """
        permission = 'cmf.ModifyPortalContent'
        if api.user.has_permission(permission, obj=self.context):
            return True
        return False

    def can_manage_portal(self):
        """
        Check is user can manage the portal.
        """
        permission = 'cmf.ManagePortal'
        if api.user.has_permission(permission, obj=self.context):
            return True
        return False

    def check_item(self, item):
        """
        Check if we want to have the given item in the navigation.
        """
        context = self.context
        if item.exclude_from_nav:
            return False
        try:
            if context.default_page == item.id:
                return False
        except AttributeError:
            pass
        return True

    def get_items(self):
        """
        Get folder contents and return.
        """
        context = self.context
        root_nav = api.portal.get_registry_record(
            name='collective.sidebar.root_nav',
            default=False,
        )
        if root_nav:
            context = api.portal.get_navigation_root(context)
        contents = []
        if IFolderish.providedBy(context):
            contents = context.getFolderContents()
        else:
            try:
                parent = context.aq_parent
                contents = parent.getFolderContents()
            except Exception:
                pass
        items = []
        for item in contents:
            if self.check_item(item):
                data = {
                    'title': item.Title,
                    'title_cropped': crop(item.Title, 100),
                    'url': item.getURL(),
                }
                items.append(data)
        return items

    def get_folder_contents_url(self):
        """
        Get URL to folder_contents.
        """
        context = self.context
        parent = context.aq_parent
        context_url = context.absolute_url() + '/folder_contents'
        parent_url = parent.absolute_url() + '/folder_contents'
        try:
            if parent.default_page == context.id:
                return parent_url
        except AttributeError:
            pass
        if IFolderish.providedBy(context):
            return context_url
        else:
            return parent_url

    def get_workflow_state_title(self):
        """
        Returns the workflow state title.
        """
        state = self.get_workflow_state()
        tools = getMultiAdapter(
            (self.context, self.request),
            name='plone_tools',
        )
        workflows = tools.workflow().getWorkflowsFor(self.context)
        if workflows:
            for w in workflows:
                if state in w.states:
                    return w.states[state].title or state

    def has_workflow(self):
        """
        Check if there is a workflow for the current context.
        """
        state = self.get_workflow_state()
        return state is not None

    def has_workflow_state_color(self):
        """
        Returns a CSS class for workflow state:
            - with-state-color
            - without-state-color
        TODO: This should be a switch in the backend # noqa: T000
              to enable colored states.
        """
        return 'with-state-color'

    def get_workflow_state(self):
        """
        Return the workflow state for the current context.
        """
        return api.content.get_state(self.context, None)

    def get_workflow_actions(self):
        """
        Return menu item entries in a TAL-friendly form.
        """
        from plone.app.contentmenu import PloneMessageFactory as _
        context = self.context
        request = context.REQUEST
        try:
            pkg_resources.get_distribution('Products.CMFPlacefulWorkflow')
            from Products.CMFPlacefulWorkflow.permissions import ManageWorkflowPolicies  # noqa: 501
        except pkg_resources.DistributionNotFound:
            from Products.CMFCore.permissions import ManagePortal as ManageWorkflowPolicies  # noqa: 501
        results = []
        locking_info = queryMultiAdapter(
            (context, request),
            name='plone_lock_info',
        )
        if locking_info and locking_info.is_locked_for_current_user():
            return []
        wf_tool = getToolByName(context, 'portal_workflow')
        workflowActions = wf_tool.listActionInfos(object=context)
        for action in workflowActions:
            if action['category'] != 'workflow':
                continue
            cssClass = ''
            actionUrl = action['url']
            if actionUrl == '':
                actionUrl = '{0}/content_status_modify?workflow_action={1}'
                actionUrl = actionUrl.format(
                    context.absolute_url(),
                    action['id'],
                )
                cssClass = ''
            description = ''
            transition = action.get('transition', None)
            if transition is not None:
                description = transition.description
            if action['allowed']:
                results.append({
                    'title': action['title'],
                    'description': description,
                    'action': addTokenToUrl(actionUrl, request),
                    'selected': False,
                    'icon': None,
                    'extra': {
                        'id': 'workflow-transition-{0}'.format(action['id']),
                        'separator': None,
                        'class': cssClass,
                    },
                    'submenu': None,
                })
        url = context.absolute_url()
        pw = getToolByName(context, 'portal_placeful_workflow', None)
        if pw is not None:
            if _checkPermission(ManageWorkflowPolicies, context):
                results.append({
                    'title': _(u'workflow_policy', default=u'Policy...'),
                    'description': '',
                    'action': url + '/placeful_workflow_configuration',
                    'selected': False,
                    'icon': None,
                    'extra': {
                        'id': 'workflow-transition-policy',
                        'separator': None,
                        'class': '',
                    },
                    'submenu': None,
                })
        return results

    @staticmethod
    def is_actions_enabled():
        """
        Should actions be shown
        """
        return api.portal.get_registry_record(
            name='collective.sidebar.enable_actions',
            default=True,
        )

    def cookies_enabled(self):
        """
        Should cookie support be enabled
        """
        return api.portal.get_registry_record(
            'collective.sidebar.enable_cookies',
            default=False,
        )

    def collapse_enabled(self):
        """
        Should collapsible sections be enabled
        """
        return api.portal.get_registry_record(
            'collective.sidebar.enable_collapse',
            default=False,
        )

    def get_section_state(self, section_name=''):
        """
        Return section 'collapsed' state
        """
        if self.cookies_enabled() and self.collapse_enabled():
            sections = self.request.get('sections', '')
            if sections:
                sections = sections.split(',')
                if section_name in sections:
                    return 'menu-section collapsed'
        return 'menu-section'

    def has_actions(self):
        """
        Checks whether there are actions to display
        """
        return len(self.get_actions()) > 0

    def get_actions(self):
        """
        Returns registred object_actions like cut, copy, paste, ...
        """
        portal = api.portal.get()
        actions = portal.portal_actions.listFilteredActionsFor(self.context)
        buttons = list()
        if actions:
            buttons = actions.get('object_buttons', list())
            for action in buttons:
                if not action.get('icon', None):
                    action.icon = get_action_icon(action.get('id', None))
                if action.get('url', None):
                    action.url = addTokenToUrl(action.get('url'), self.request)
        return buttons

    def get_addable_items(self):
        """
        Return menu item entries in a TAL-friendly form.
        """
        context = self.context
        request = self.request
        factories_view = getMultiAdapter(
            (context, request),
            name='folder_factories',
        )
        include = None
        addContext = factories_view.add_context()
        constraints = IConstrainTypes(addContext, None)
        if constraints is not None:
            include = constraints.getImmediatelyAddableTypes()
        results = factories_view.addable_types(include=include)
        results_with_icons = []
        for result in results:
            result['icon'] = 'menu-item-icon glyphicon glyphicon-plus'
            results_with_icons.append(result)
        results = results_with_icons
        constraints = ISelectableConstrainTypes(addContext, None)
        if constraints is not None:
            if constraints.canSetConstrainTypes() and \
                    constraints.getDefaultAddableTypes():
                url = '{0}/folder_constraintypes_form'.format(
                    addContext.absolute_url(),
                )
                results.append({
                    'title': _(u'folder_add_settings',
                               default=u'Restrictions'),
                    'description': _(
                        u'title_configure_addable_content_types',
                        default=u'Configure which content types can be '
                                u'added here',
                    ),
                    'action': url,
                    'selected': False,
                    'icon': 'menu-item-icon glyphicon glyphicon-cog',
                    'id': 'settings',
                    'extra': {
                        'id': 'plone-contentmenu-settings',
                        'separator': None,
                        'class': '',
                    },
                    'submenu': None,
                })
        # Also add a menu item to add items to the default page
        context_state = getMultiAdapter(
            (context, request),
            name='plone_context_state',
        )
        if context_state.is_structural_folder() and \
                context_state.is_default_page() and \
                self._contentCanBeAdded(context, request):
            results.append({
                'title': _(u'default_page_folder',
                           default=u'Add item to default page'),
                'description': _(
                    u'desc_default_page_folder',
                    default=u'If the default page is also a folder, '
                            u'add items to it from here.',
                ),
                'action': context.absolute_url() + '/@@folder_factories',
                'selected': False,
                'icon': 'menu-item-icon glyphicon glyphicon-cog',
                'id': 'special',
                'extra': {
                    'id': 'plone-contentmenu-add-to-default-page',
                    'separator': None,
                    'class': 'pat-plone-modal',
                },
                'submenu': None,
            })
        return results

    def _get_context_state(self):
        return getMultiAdapter((self.context, self.request),
                               name='plone_context_state')

    def get_default_view_link(self):
        context_state = self._get_context_state()
        if context_state.is_default_page():
            parent = context_state.parent()
            return parent.absolute_url() + '/select_default_view'
        else:
            return self.context.absolute_url() + '/select_default_view'

    def get_default_page_link(self):
        context_state = self._get_context_state()
        if context_state.is_default_page():
            parent = context_state.parent()
            return parent.absolute_url() + '/select_default_page'
        else:
            return self.context.absolute_url() + '/select_default_page'


def get_action_icon(id1):
    """
    Returns icons for action ids
    """
    icon_map = {
        'cut': 'glyphicon glyphicon-scissors',
        'copy': 'glyphicon glyphicon-duplicate',
        'paste': 'glyphicon glyphicon-open-file',
        'delete': 'glyphicon glyphicon-trash',
        'rename': 'glyphicon glyphicon-random',
        'ical_import_enable': 'glyphicon glyphicon-calendar',
        'ical_import_disable': 'glyphicon glyphicon-calendar',
    }
    if id1 and id1 in icon_map:
        return icon_map[id1]
    else:
        return 'glyphicon glyphicon-star'


class SidebarAJAX(BrowserView):

    def __call__(self, render):
        context = self.context
        request = self.request
        if render:
            return self.render_viewlet(context, request)
        return

    def render_viewlet(self, context, request):
        navigation = SidebarViewlet(context, request, None, None)
        return navigation.render()


class CoverViewlet(SidebarViewlet):
    index = ViewPageTemplateFile('templates/cover.pt')
