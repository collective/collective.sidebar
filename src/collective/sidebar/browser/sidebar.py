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
        return api.user.is_anonymous()

    def get_portal_url(self):
        return api.portal.get().absolute_url()

    def get_user_profile_url(self):
        return api.portal.get().absolute_url() + get_user()[2]

    def get_search_path(self, query=False):
        if query:
            return api.portal.get().absolute_url() + '/@@search?SearchableText='  # noqa :501
        return api.portal.get().absolute_url() + '/@@search'

    def get_navigation_root_url(self):
        """
        Return navigation root URL based on the language.
        """
        navigation_root = api.portal.get_navigation_root(self.context)
        return navigation_root.absolute_url()

    def get_language(self):
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
        if hasattr(parent, 'default_page'):
            if parent.default_page == self.context.id:
                if parent == api.portal.get_navigation_root(self.context):
                    return None
                else:
                    return parent.aq_parent.absolute_url()
        return parent.absolute_url()

    def can_edit(self):
        permission = 'cmf.ModifyPortalContent'
        if api.user.has_permission(permission, obj=self.context):
            return True
        return False

    def can_manage_portal(self):
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
        if hasattr(context, 'default_page'):
            if context.default_page == item.id:
                return False
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
        title_filter = [
            'Collection',
            'News Folder',
            'Frontpage',
            'Sponsors',
            'Tracks',
            'Events',
        ]
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
                if hasattr(parent, 'default_page'):
                    if parent.default_page == context.id:
                        url = parent_url
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
        if hasattr(parent, 'default_page'):
            if parent.default_page == context.id:
                return parent_url
        if IFolderish.providedBy(context):
            return context_url
        else:
            return parent_url
