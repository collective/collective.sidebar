# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from datetime import datetime
from datetime import timedelta
from collective.sidebar import _
from plone import api
from zope.i18n import translate


def get_translated(text, context, domain='plone', multi_domain=False):
    if context:
        language_id = context.request.response.headers.get('content-language', None)  # noqa: 501
        if language_id:
            translated = translate(
                text, domain=domain, target_language=language_id)
            if multi_domain:
                if translated != text:
                    return translated
                package_domain = _._domain
                package_translated = translate(
                    text, domain=package_domain, target_language=language_id)
                if package_translated != text:
                    return package_translated
            return translated
    return text

def crop(text, count):
    """Crop given text to given count"""
    cropped_text = ' '.join((text[0:count].strip()).split(' ')[:-1])
    strips = ['.', ',', ':', ';']
    for s in strips:
        cropped_text = cropped_text.strip(s)
    if len(text) > count:
        return cropped_text + u'...'
    return text

def get_user():
    """Return MemberData, ID and profile directory for the current user"""
    user = api.user.get_current()
    user_id = user.id
    user_dir = '/users/{0}'.format(user_id)
    return user, user_id, user_dir
