# -*- coding: utf-8 -*-

from collective.sidebar import _
from collective.sidebar.controlpanel.config import PositionVocabulary
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IControlPanel(Interface):

    enable_navigation = schema.Bool(
        title=_(
            u'controlpanel_sidebar_show_navigation_title',
            default='Show Navigation Section',
        ),
        description=_(
            u'controlpanel_sidebar_show_navigation_description',
            default=(
                u'Show navigation section.'
            ),
        ),
        required=False,
        default=True,
    )

    root_nav = schema.Bool(
        title=_(
            u'controlpanel_sidebar_show_root_nav_title',
            default='Root Level Navigation',
        ),
        description=_(
            u'controlpanel_sidebar_show_root_nav_description',
            default=(
                u'When enabled, the sidebar will display '
                u'the root level navigation.'
            ),
        ),
        required=False,
        default=False,
    )

    dynamic_navigation = schema.Bool(
        title=_(
            u'controlpanel_sidebar_dynamic_navigation_title',
            default='Enable dynamic Navigation',
        ),
        description=_(
            u'controlpanel_sidebar_dynamic_navigation_description',
            default=(u'Enable dynamic navigation inside sidebar.'),
        ),
        required=False,
        default=True,
    )

    enable_actions = schema.Bool(
        title=_(
            u'controlpanel_sidebar_show_actions_title',
            default='Show Actions Section',
        ),
        description=_(
            u'controlpanel_sidebar_show_actions_description',
            default=(
                u'Show actions section including object '
                u'buttons for cut, copy, paste, etc.'
            ),
        ),
        required=False,
        default=True,
    )

    enable_collapse = schema.Bool(
        title=_(
            u'controlpanel_sidebar_enable_collapse_title',
            default='Collapsible Sections',
        ),
        description=_(
            u'controlpanel_sidebar_enable_collapse_description',
            default=(
                u'When enabled, the sidebar sections can be collapsed. '
                u'This feature is only available when cookies are enabled.'
            ),
        ),
        required=False,
        default=True,
    )

    sidebar_position = schema.Choice(
        title=_(
            u'controlpanel_sidebar_sidebar_position_title',
            default='Sidebar Position',
        ),
        description=_(
            u'controlpanel_sidebar_sidebar_position_description',
            default=u'Display the sidebar on the left or right.',
        ),
        vocabulary=PositionVocabulary,
        required=True,
        default='start',
    )

    mouse = schema.Bool(
        title=_(
            u'controlpanel_mouse_title',
            default='Mouse activated',
        ),
        description=_(
            u'controlpanel_mouse_description',
            default=(u'When enabled, the sidebar will be opened by mouse.'),
        ),
        required=False,
        default=True,
    )

    mouse_area = schema.Int(
        title=_(
            u'controlpanel_mouse_area_title',
            default='Mouse Activation Area',
        ),
        description=_(
            u'controlpanel_mouse_area_description',
            default=(u'Enter the number of pixels to activate the sidebar.'),
        ),
        required=False,
        default=30,
    )


class ControlPanelEditForm(RegistryEditForm):
    schema = IControlPanel
    schema_prefix = 'collective.sidebar'
    label = _(u'collective_sidebar_title', default=u'Collective Sidebar')


ControlPanelView = layout.wrap_form(
    ControlPanelEditForm,
    ControlPanelFormWrapper,
)
