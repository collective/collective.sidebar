# -*- coding: utf-8 -*-

from collective.sidebar import _
from plone import api
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


def get_workflow_data(context):
    """
    Return the workflow data for the context.
    """
    portal_workflow = api.portal.get_tool('portal_workflow')
    workflows = portal_workflow.getWorkflowsFor(context)
    result = {
        'state': '',
        'transitions': list(),
    }
    if workflows:
        workflow = workflows[0]
        state = api.content.get_state(context, None)
        transitions = getattr(workflow.states, state).transitions
        result['state'] = state
        result['transitions'] = transitions
    return result
