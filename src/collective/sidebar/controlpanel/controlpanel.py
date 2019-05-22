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
            default='Root Navigation',
        ),
        description=_(
            u'controlpanel_sidebar_show_root_nav_description',
            default=(
                u'When enabled, the sidebar will always '
                u'display the root level navigation.'
            ),
        ),
        required=False,
        default=False,
    )

    enable_actions = schema.Bool(
        title=_(
            u'controlpanel_sidebar_show_actions_title',
            default='Show Actions',
        ),
        description=_(
            u'controlpanel_sidebar_show_actions_description',
            default=(
                u'When enabled, the sidebar will '
                u'display registered actions like cut, copy and paste...'
            ),
        ),
        required=False,
        default=True,
    )

    enable_cookies = schema.Bool(
        title=_(
            u'controlpanel_sidebar_enable_cookies_title',
            default='Enable Cookie Features',
        ),
        description=_(
            u'controlpanel_sidebar_enable_cookies_description',
            default=u'Enable or disable cookies for sidebar enhancements.',
        ),
        required=False,
        default=False,
    )

    enable_collapse = schema.Bool(
        title=_(
            u'controlpanel_sidebar_enable_collapse_title',
            default='Enable Collapsible Sections',
        ),
        description=_(
            u'controlpanel_sidebar_enable_collapse_description',
            default=(
                u'When enabled, the sidebar sections can be collapsed'
                u'or expanded. This feature is only available '
                u'with cookie features enabled.'
            ),
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
