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
