# -*- coding: utf-8 -*-

from collective.sidebar import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IControlPanel(Interface):

    root_nav = schema.Bool(
        title=_(
            u'controlpanel_sidebar_show_root_nav_title',
            default='Root Level Navigation',
        ),
        description=_(
            u'controlpanel_sidebar_show_root_nav_description',
            default=(u'When enabled, the sidebar will display the root level navigation.'),  # noqa: 501
        ),
        required=False,
        default=False,
    )

    enable_actions = schema.Bool(
        title=_(
            u'controlpanel_sidebar_show_actions_title',
            default='Show Actions Section',
        ),
        description=_(
            u'controlpanel_sidebar_show_actions_description',
            default=(u'Show actions section including object buttons for cut, copy, paste, etc.'),  # noqa: 501
        ),
        required=False,
        default=True,
    )

    enable_cookies = schema.Bool(
        title=_(
            u'controlpanel_sidebar_enable_cookies_title',
            default='Enable Cookies',
        ),
        description=_(
            u'controlpanel_sidebar_enable_cookies_description',
            default=u'Enable cookies for sidebar features.',
        ),
        required=False,
        default=False,
    )

    enable_collapse = schema.Bool(
        title=_(
            u'controlpanel_sidebar_enable_collapse_title',
            default='Collapsible Sections',
        ),
        description=_(
            u'controlpanel_sidebar_enable_collapse_description',
            default=(u'When enabled, the sidebar sections can be collapsed. This feature is only available when cookies are enabled.'),  # noqa: 501
        ),
        required=False,
        default=False,
    )


class ControlPanelEditForm(RegistryEditForm):
    schema = IControlPanel
    schema_prefix = 'collective.sidebar'
    label = _(u'collective_sidebar_title', default=u'Collective Sidebar')


ControlPanelView = layout.wrap_form(
    ControlPanelEditForm,
    ControlPanelFormWrapper,
)
