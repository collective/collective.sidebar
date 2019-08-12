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

    icon_font = schema.Choice(
        title=_(u'controlpanel_sidebar_choose_icon_font_title',
                default=u'Choose Icon Font'),
        description=_(
            u'controlpanel_sidebar_choose_icon_font_description',
            default=(
                u'When you installed a different icon font, you can tell '
                u'sidebar here to use it. For Fontello we assume you set '
                u'"icon" as font name')
        ),
        values=('Glyphicons', 'Fontello', 'Font Awesome', 'Font Awesome Pro', 'Font Awesome Light'),  # noqa: 501
        default='Glyphicons',
        required=True
    )


class ControlPanelEditForm(RegistryEditForm):
    schema = IControlPanel
    schema_prefix = 'collective.sidebar'
    label = _(u'collective_sidebar_title', default=u'Collective Sidebar')


ControlPanelView = layout.wrap_form(
    ControlPanelEditForm,
    ControlPanelFormWrapper,
)
