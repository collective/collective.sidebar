# -*- coding: utf-8 -*-
import math
import pytz
from Products.ATContentTypes.utils import DT2dt
from collective.sidebar.utils import crop
from collective.sidebar.utils import get_translated
from collective.sidebar.utils import get_user
from collective.sidebar import _
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from datetime import datetime


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

    def get_last_modified(self):
        try:
            date = self.context.modified()
            date = DT2dt(date)  # zope DateTime -> python datetime
            now = datetime.utcnow()
            now = now.replace(tzinfo=pytz.utc)

            delta = now - date
            seconds = delta.seconds + delta.microseconds / 1E6 + delta.days * 86400
            days = math.floor(seconds / (3600 * 24))

            if days <= 0 and seconds <= 0:
                ret_string = ''
            elif days > 7:
                return date.strftime('%d.%m.%Y %H:%M')  # 1.3.2017 10:30
            elif days >= 1:
                return date.strftime('%A %H:%M')  # Tuesday 10:30
            else:
                hours = math.floor(seconds / 3600.0)
                minutes = math.floor((seconds % 3600) / 60)
                if hours > 1:
                    ret_string = _(u'sidebar_msg_x_hours_x_minutes_ago',
                                   default=u'${hours} hours ${minutes} minutes ago',
                                   mapping={u'hours': int(hours), u'minutes': int(minutes)})
                elif hours == 1:
                    ret_string = _(u'sidebar_msg_one_hour_x_minutes_ago', default=u'$An hour {minutes} minutes ago',
                                   mapping={u'minutes': int(minutes)})
                else:
                    if minutes > 1:
                        ret_string = _(u'sidebar_msg_x_minutes_ago', default=u'${minutes} minutes ago',
                                       mapping={u'minutes': int(minutes)})
                    elif minutes == 1:
                        ret_string = _(u'sidebar_msg_one_minute_ago', default=u'a minute ago')
                    else:
                        ret_string = _(u'sidebar_msg_seconds_ago', default=u'a few seconds ago')
        except AttributeError:
            ret_string = _(u'sidebar_msg_history', default=u'History')

        return self.context.translate(ret_string)


class CoverViewlet(SidebarViewlet):
    index = ViewPageTemplateFile('templates/cover.pt')
