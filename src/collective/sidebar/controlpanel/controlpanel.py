# -*- coding: utf-8 -*-

from collective.sidebar import _
from collective.sidebar.controlpanel.config import fontVocabulary
from collective.sidebar.controlpanel.config import positionVocabulary
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

    icon_font = schema.Choice(
        title=_(u'controlpanel_sidebar_choose_icon_font_title',
                default=u'Choose Icon Font'),
        description=_(
            u'controlpanel_sidebar_choose_icon_font_description',
            default=(
                u'When a different icon font is installed, you can tell the '
                u'sidebar to use it. For Fontello we assume you have set '
                u'\"icon\" as the font prefix. '
                u'Note: This does not install the icon font!'),
        ),
        vocabulary=fontVocabulary,
        default='Glyphicons',
        required=True,
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
        vocabulary=positionVocabulary,
        required=True,
        default='left',
    )


class ControlPanelEditForm(RegistryEditForm):
    schema = IControlPanel
    schema_prefix = 'collective.sidebar'
    label = _(u'collective_sidebar_title', default=u'Collective Sidebar')


ControlPanelView = layout.wrap_form(
    ControlPanelEditForm,
    ControlPanelFormWrapper,
)
