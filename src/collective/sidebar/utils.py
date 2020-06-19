# -*- coding: utf-8 -*-

from collective.sidebar.config import ICONS
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
    text = '{a} {b}'.format(a=ICONS['__prefix__'][icon_font], b=icon)
    if icon in ICONS:
        values = ICONS[icon]
        if icon_font in values:
            text = values[icon_font]
    return text
