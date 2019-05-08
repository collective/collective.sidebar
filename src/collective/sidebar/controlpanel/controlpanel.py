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
                'display the root level navigation.'
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
                'display registred object_buttons actions '
                'like cut, copy, paste, ...'
            ),
        ),
        required=False,
        default=True,
    )


class ControlPanelEditForm(RegistryEditForm):
    schema = IControlPanel
    schema_prefix = 'collective.sidebar'
    label = _(u'collective_sidebar_title', default=u'Collective Sidebar')


ControlPanelView = layout.wrap_form(
    ControlPanelEditForm,
    ControlPanelFormWrapper,
)
