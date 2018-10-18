# -*- coding: utf-8 -*-

from collective.sidebar.utils import crop
from collective.sidebar.utils import get_translated
from collective.sidebar.utils import get_user
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SidebarViewlet(ViewletBase):

    index = ViewPageTemplateFile('templates/sidebar.pt')

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

    def get_user_profile_url(self):
        """
        Return URL for the user profile.
        """
        portal_url = self.get_portal_url()
        portal_user = get_user()[2]
        return portal_url + portal_user

    def get_search_path(self, query=False):
        """
        Return a search URL using the SearchableText attribute.
        """
        portal_url = self.get_portal_url()
        if query:
            return '{0}/@@search?SearchableText='.format(portal_url)
        return '{0}/@@search'.format(portal_url)

    def get_navigation_root_url(self):
        """
        Return navigation root URL based on the language.
        """
        navigation_root = api.portal.get_navigation_root(self.context)
        return navigation_root.absolute_url()

    def get_language(self):
        """
        Return the current language.
        """
        return api.portal.get_current_language()

    def get_back(self):
        """
        Get link to parent.
        """
        parent = self.context.aq_parent
        if self.context == api.portal.get():
            return None
        if self.context.portal_type == 'LRF':
            return None
        try:
            if parent.default_page == self.context.id:
                if parent == api.portal.get_navigation_root(self.context):
                    return None
                else:
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

    def get_items(self, root=False):
        """
        Get folder contents and return.
        """
        context = self.context
        if root:
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

    def get_addable_types(self):
        """
        Get addable Content-Types.
        """
        context = self.context
        parent = context.aq_parent
        context_url = context.absolute_url()
        parent_url = parent.absolute_url()
        # Filter for Content-Types
        title_filter = []
        factories = api.content.get_view(
            'plone.contentmenu.factories',
            self.context,
            self.request,
        )
        addable_types = factories._addableTypesInContext(self.context)
        data = []
        for item in addable_types:
            title = item.id
            if title in title_filter:
                pass
            else:
                url = context_url
                try:
                    if parent.default_page == context.id:
                        url = parent_url
                except AttributeError:
                    pass
                url = '{0}/++add++{1}'.format(url, title)
                data.append({'title': get_translated(title, self), 'url': url})
        return data

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

    def get_workflow_data(self):
        """
        Return the workflow data for the context.
        """
        portal_workflow = api.portal.get_tool('portal_workflow')
        transitions = portal_workflow.getTransitionsFor(self.context)
        result = {
            'state': {
                'name': '',
                'color': 'sidebar-blue',
            },
            'transitions': [],
        }
        if transitions:
            # Get the current state
            state = api.content.get_state(self.context, None)
            # Set a color for the state
            if state == 'private':
                result['state']['color'] = 'sidebar-red'
            elif state == 'pending':
                result['state']['color'] = 'sidebar-yellow'
            elif state == 'visible':
                result['state']['color'] = 'sidebar-purple'
            result['state']['name'] = get_translated(state, self)
            result['transitions'] = transitions
        return result

    def getMenuItems(self):
        """Return menu item entries in a TAL-friendly form."""
        context = self.context
        request = context.REQUEST
        from plone.app.contentmenu import PloneMessageFactory as _
        from zope.component import queryMultiAdapter
        from Products.CMFCore.utils import getToolByName
        from plone.protect.utils import addTokenToUrl
        from Products.CMFCore.utils import _checkPermission
        import pkg_resources
        try:
            pkg_resources.get_distribution('Products.CMFPlacefulWorkflow')
            from Products.CMFPlacefulWorkflow.permissions import \
                ManageWorkflowPolicies
        except pkg_resources.DistributionNotFound:
            from Products.CMFCore.permissions import \
                ManagePortal as ManageWorkflowPolicies  # noqa

        results = []

        locking_info = queryMultiAdapter((context, request),
                                         name='plone_lock_info')
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
                        'class': cssClass},
                    'submenu': None,
                })

        url = context.absolute_url()

        if len(results) > 0:
            results.append({
                'title': _(u'label_advanced', default=u'Advanced...'),
                'description': '',
                'action': url + '/content_status_history',
                'selected': False,
                'icon': None,
                'extra': {
                    'id': 'workflow-transition-advanced',
                    'separator': 'actionSeparator',
                    'class': 'pat-plone-modal'},
                'submenu': None,
            })

        pw = getToolByName(context, 'portal_placeful_workflow', None)
        if pw is not None:
            if _checkPermission(ManageWorkflowPolicies, context):
                results.append({
                    'title': _(u'workflow_policy',
                               default=u'Policy...'),
                    'description': '',
                    'action': url + '/placeful_workflow_configuration',
                    'selected': False,
                    'icon': None,
                    'extra': {'id': 'workflow-transition-policy',
                              'separator': None,
                              'class': ''},
                    'submenu': None,
                })

        return results


class CoverViewlet(SidebarViewlet):

    index = ViewPageTemplateFile('templates/cover.pt')
