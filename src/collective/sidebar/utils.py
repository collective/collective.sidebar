# -*- coding: utf-8 -*-

from plone import api


def crop(text, max_char_length):
    """
    Crop given text by full words to given count of chars.
    """
    if len(text) > max_char_length:
        cleared_text = text
        special_chars = [u'.', u',', u':', u';']
        for s in special_chars:
            cleared_text = cleared_text.replace(s, u' ')
        cropped_text = u' '.join((cleared_text[0:max_char_length].strip()).split(u' ')[:-1])  # noqa
        if len(cropped_text) == 0:
            cropped_text = cleared_text[0:max_char_length].strip()
        return cropped_text + u'...'
    return text


def get_user():
    """
    Return MemberData, ID and profile directory for the current user.
    """
    user = api.user.get_current()
    user_id = user.id
    user_dir = '/users/{0}'.format(user_id)
    return user, user_id, user_dir


def get_icon(icon):
    """
    Returns a css class for the icon. Reads the icon font from the registry.
    """
    # Possible icon font values? See src/collective/sidebar/controlpanel/controlpanel.py:76  # noqa: 501
    icon_font = api.portal.get_registry_record(
        name='collective.sidebar.icon_font',
        default='Glyphicons',
    )
    text = '{a} {b}'.format(a=icon_dict['__prefix__'][icon_font], b=icon)
    if icon in icon_dict:
        values = icon_dict[icon]
        if icon_font in values:
            text = values[icon_font]
    return text


icon_dict = {
    '__prefix__': {
        'Glyphicons': 'glyphicon',
        'Fontello': 'icon',
        'Font Awesome': 'fas',
        'Font Awesome Pro': 'far',
        'Font Awesome Light': 'fal',
        'Font Awesome Duotone': 'fad',
    },
    'cut': {
        'Glyphicons': 'glyphicon glyphicon-scissors',
        'Fontello': 'icon cut',
        'Font Awesome': 'fas fa-cut',
        'Font Awesome Pro': 'far fa-cut',
        'Font Awesome Light': 'fal fa-cut',
        'Font Awesome Duotone': 'fad fa-cut',
    },
    'copy': {
        'Glyphicons': 'glyphicon glyphicon-duplicate',
        'Fontello': 'icon copy',
        'Font Awesome': 'far fa-copy',
        'Font Awesome Pro': 'far fa-copy',
        'Font Awesome Light': 'fal fa-copy',
        'Font Awesome Duotone': 'fad fa-copy',
    },
    'paste': {
        'Glyphicons': 'glyphicon glyphicon-open-file',
        'Fontello': 'icon paste',
        'Font Awesome': 'far fa-clipboard',
        'Font Awesome Pro': 'far fa-paste',
        'Font Awesome Light': 'fal fa-paste',
        'Font Awesome Duotone': 'fad fa-paste',
    },
    'delete': {
        'Glyphicons': 'glyphicon glyphicon-trash',
        'Fontello': 'icon delete',
        'Font Awesome': 'far fa-trash-alt',
        'Font Awesome Pro': 'far fa-trash-alt',
        'Font Awesome Light': 'fal fa-trash-alt',
        'Font Awesome Duotone': 'fad fa-trash-alt',
    },
    'rename': {
        'Glyphicons': 'glyphicon glyphicon-random',
        'Fontello': 'icon rename',
        'Font Awesome': 'fas fa-random',
        'Font Awesome Pro': 'far fa-random',
        'Font Awesome Light': 'fal fa-random',
        'Font Awesome Duotone': 'fad fa-random',
    },
    'ical_import_enable': {
        'Glyphicons': 'glyphicon glyphicon-calendar',
        'Fontello': 'icon calendar',
        'Font Awesome': 'far fa-calendar',
        'Font Awesome Pro': 'far fa-calendar',
        'Font Awesome Light': 'fal fa-calendar',
        'Font Awesome Duotone': 'fad fa-calendar',
    },
    'ical_import_disable': {
        'Glyphicons': 'glyphicon glyphicon-calendar',
        'Fontello': 'icon calendar',
        'Font Awesome': 'far fa-calendar',
        'Font Awesome Pro': 'far fa-calendar',
        'Font Awesome Light': 'fal fa-calendar',
        'Font Awesome Duotone': 'fad fa-calendar',
    },
    'star': {
        'Glyphicons': 'glyphicon glyphicon-star',
        'Fontello': 'icon star',
        'Font Awesome': 'far fa-star',
        'Font Awesome Pro': 'far fa-star',
        'Font Awesome Light': 'fal fa-star',
        'Font Awesome Duotone': 'fad fa-star',
    },
    'menu-down': {
        'Glyphicons': 'glyphicon glyphicon-menu-down',
        'Fontello': 'icon menu-down',
        'Font Awesome': 'fas fa-sort-down',
        'Font Awesome Pro': 'far fa-sort-down',
        'Font Awesome Light': 'fal fa-sort-down',
        'Font Awesome Duotone': 'fad fa-sort-down',
    },
    'menu-up': {
        'Glyphicons': 'glyphicon glyphicon-menu-up',
        'Fontello': 'icon menu-up',
        'Font Awesome': 'fas fa-sort-up',
        'Font Awesome Pro': 'far fa-sort-up',
        'Font Awesome Light': 'fal fa-sort-up',
        'Font Awesome Duotone': 'fad fa-sort-up',
    },
    'menu-left': {
        'Glyphicons': 'glyphicon glyphicon-menu-left',
        'Fontello': 'icon menu-left',
        'Font Awesome': 'fas fa-angle-left',
        'Font Awesome Pro': 'far fa-angle-left',
        'Font Awesome Light': 'fal fa-angle-left',
        'Font Awesome Duotone': 'fad fa-angle-left',
    },
    'menu-right': {
        'Glyphicons': 'glyphicon glyphicon-menu-right',
        'Fontello': 'icon menu-right',
        'Font Awesome': 'fas fa-angle-right',
        'Font Awesome Pro': 'far fa-angle-right',
        'Font Awesome Light': 'fal fa-angle-right',
        'Font Awesome Duotone': 'fad fa-angle-right',
    },
    'cog': {
        'Glyphicons': 'glyphicon glyphicon-cog',
        'Fontello': 'icon cog',
        'Font Awesome': 'fas fa-cog',
        'Font Awesome Pro': 'far fa-cog',
        'Font Awesome Light': 'fal fa-cog',
        'Font Awesome Duotone': 'fad fa-cog',
    },
    'eye-open': {
        'Glyphicons': 'glyphicon glyphicon-eye-open',
        'Fontello': 'icon eye-open',
        'Font Awesome': 'far fa-eye',
        'Font Awesome Pro': 'far fa-eye',
        'Font Awesome Light': 'fal fa-eye',
        'Font Awesome Duotone': 'fad fa-eye',
    },
    'edit': {
        'Glyphicons': 'glyphicon glyphicon-edit',
        'Fontello': 'icon edit',
        'Font Awesome': 'far fa-edit',
        'Font Awesome Pro': 'far fa-edit',
        'Font Awesome Light': 'fal fa-edit',
        'Font Awesome Duotone': 'fad fa-edit',
    },
    'folder-open': {
        'Glyphicons': 'glyphicon glyphicon-folder-open',
        'Fontello': 'icon folder-open',
        'Font Awesome': 'far fa-folder-open',
        'Font Awesome Pro': 'far fa-folder-open',
        'Font Awesome Light': 'fal fa-folder-open',
        'Font Awesome Duotone': 'fad fa-folder-open',
    },
    'time': {
        'Glyphicons': 'glyphicon glyphicon-time',
        'Fontello': 'icon time',
        'Font Awesome': 'far fa-clock',
        'Font Awesome Pro': 'far fa-clock',
        'Font Awesome Light': 'fal fa-clock',
        'Font Awesome Duotone': 'fad fa-clock',
    },
    'user': {
        'Glyphicons': 'glyphicon glyphicon-user',
        'Fontello': 'icon user',
        'Font Awesome': 'far fa-user',
        'Font Awesome Pro': 'far fa-user',
        'Font Awesome Light': 'fal fa-user',
        'Font Awesome Duotone': 'fad fa-user',
    },
    'share': {
        'Glyphicons': 'glyphicon glyphicon-user',
        'Fontello': 'icon share',
        'Font Awesome': 'fas fa-share-alt',
        'Font Awesome Pro': 'far fa-share-alt',
        'Font Awesome Light': 'fal fa-share-alt',
        'Font Awesome Duotone': 'fad fa-share-alt',
    },
    'record': {
        'Glyphicons': 'glyphicon glyphicon-record',
        'Fontello': 'icon record',
        'Font Awesome': 'fas fa-bullseye',
        'Font Awesome Pro': 'far fa-bullseye',
        'Font Awesome Light': 'fal fa-bullseye',
        'Font Awesome Duotone': 'fad fa-bullseye',
    },
    'transfer': {
        'Glyphicons': 'glyphicon glyphicon-transfer',
        'Fontello': 'icon transfer',
        'Font Awesome': 'fas fa-exchange-alt',
        'Font Awesome Pro': 'far fa-exchange',
        'Font Awesome Light': 'fal fa-exchange',
        'Font Awesome Duotone': 'fad fa-exchange',
    },
    'option-horizontal': {
        'Glyphicons': 'glyphicon glyphicon-option-horizontal',
        'Fontello': 'icon option-horizontal',
        'Font Awesome': 'fas fa-toolbox',
        'Font Awesome Pro': 'far fa-toolbox',
        'Font Awesome Light': 'fal fa-toolbox',
        'Font Awesome Duotone': 'fad fa-toolbox',
    },
    'blackboard': {
        'Glyphicons': 'glyphicon glyphicon-blackboard',
        'Fontello': 'icon blackboard',
        'Font Awesome': 'fas fa-chalkboard',
        'Font Awesome Pro': 'far fa-chalkboard',
        'Font Awesome Light': 'fal fa-chalkboard',
        'Font Awesome Duotone': 'fad fa-chalkboard',
    },
    'pushpin': {
        'Glyphicons': 'glyphicon glyphicon-pushpin',
        'Fontello': 'icon pushpin',
        'Font Awesome': 'fas fa-thumbtack',
        'Font Awesome Pro': 'far fa-thumbtack',
        'Font Awesome Light': 'fal fa-thumbtack',
        'Font Awesome Duotone': 'fad fa-thumbtack',
    },
    'plus': {
        'Glyphicons': 'glyphicon glyphicon-plus',
        'Fontello': 'icon plus',
        'Font Awesome': 'fas fa-plus',
        'Font Awesome Pro': 'far fa-plus',
        'Font Awesome Light': 'fal fa-plus',
        'Font Awesome Duotone': 'fad fa-plus',
    },

}
