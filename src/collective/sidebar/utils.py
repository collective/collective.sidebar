# -*- coding: utf-8 -*-

from plone import api


def crop(text, count):
    """
    Crop given text to given count.
    """
    cropped_text = ' '.join((text[0:count].strip()).split(' ')[:-1])
    strips = ['.', ',', ':', ';']
    for s in strips:
        cropped_text = cropped_text.strip(s)
    if len(text) > count:
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
    possible values=('Glyphicons', 'Fontello', 'Font Awesome', 'Font Awesome Pro', 'Font Awesome Light'),  # noqa: 501
    """
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
        'Font Awesome': 'far',
        'Font Awesome Pro': 'fap',
        'Font Awesome Light': 'fal',
    },
    'cut': {
        'Glyphicons': 'glyphicon glyphicon-scissors',
        'Fontello': 'icon cut',
        'Font Awesome': 'fas fa-cut',
        'Font Awesome Pro': 'fap fa-cut',
        'Font Awesome Light': 'fal fa-cut',
    },
    'copy': {
        'Glyphicons': 'glyphicon glyphicon-duplicate',
        'Fontello': 'icon copy',
        'Font Awesome': 'far fa-copy',
        'Font Awesome Pro': 'fap fa-copy',
        'Font Awesome Light': 'fal fa-copy',
    },
    'paste': {
        'Glyphicons': 'glyphicon glyphicon-open-file',
        'Fontello': 'icon paste',
        'Font Awesome': 'fas fa-paste',
        'Font Awesome Pro': 'fap fa-paste',
        'Font Awesome Light': 'fal fa-paste',
    },
    'delete': {
        'Glyphicons': 'glyphicon glyphicon-trash',
        'Fontello': 'icon delete',
        'Font Awesome': 'far fa-trash-alt',
        'Font Awesome Pro': 'fap fa-trash-alt',
        'Font Awesome Light': 'fal fa-trash-alt',
    },
    'rename': {
        'Glyphicons': 'glyphicon glyphicon-random',
        'Fontello': 'icon rename',
        'Font Awesome': 'fas fa-random',
        'Font Awesome Pro': 'fap fa-random',
        'Font Awesome Light': 'fal fa-random',
    },
    'ical_import_enable': {
        'Glyphicons': 'glyphicon glyphicon-calendar',
        'Fontello': 'icon calendar',
        'Font Awesome': 'fas fa-calendar',
        'Font Awesome Pro': 'fap fa-calendar',
        'Font Awesome Light': 'fal fa-calendar',
    },
    'ical_import_disable': {
        'Glyphicons': 'glyphicon glyphicon-calendar',
        'Fontello': 'icon calendar',
        'Font Awesome': 'fas fa-calendar',
        'Font Awesome Pro': 'fap fa-calendar',
        'Font Awesome Light': 'fal fa-calendar',
    },
    'star': {
        'Glyphicons': 'glyphicon glyphicon-star',
        'Fontello': 'icon ',
        'Font Awesome': 'far ',
        'Font Awesome Pro': 'fap ',
        'Font Awesome Light': 'fal ',
    },
    '': {
        'Glyphicons': 'glyphicon ',
        'Fontello': 'icon ',
        'Font Awesome': 'far ',
        'Font Awesome Pro': 'fap ',
        'Font Awesome Light': 'fal ',
    },

}
