# -*- coding: utf-8 -*-

from collective.sidebar import _
from collective.sidebar.directives import AVATAR_KEY
from plone import api
from zope import schema
from zope.i18n import translate


def get_translated(text, context, domain='plone', multi_domain=False):
    """
    Useful for multi-domain translations.
    e.g. Fetching Plone default translations.
    """
    if context:
        request = context.request
        language_id = request.response.headers.get('content-language', None)
        if language_id:
            translated = translate(
                text,
                domain=domain,
                target_language=language_id,
            )
            if multi_domain:
                if translated != text:
                    return translated
                package_domain = _._domain
                package_translated = translate(
                    text,
                    domain=package_domain,
                    target_language=language_id,
                )
                if package_translated != text:
                    return package_translated
            return translated
    return text


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


def user_avatar(iface, field_name):
    """
    Mark a field in the existing interface as the avatar image provider.
    """
    if schema.getFields(iface).get(field_name) is None:
        dottedname = '.'.join((iface.__module__, iface.__name__))
        raise AttributeError(
            '{0} has no field "{1}"'.format(
                dottedname,
                field_name
            )
        )
    store = iface.queryTaggedValue(AVATAR_KEY)
    if store is None:
        store = []
    store.append((iface, field_name, 'true'))
    iface.setTaggedValue(AVATAR_KEY, store)
