# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging


logger = logging.getLogger('collective.sidebar')


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-collective.sidebar:default',
    )


def to_1001(context):
    context.runAllImportStepsFromProfile('profile-collective.sidebar:to_1001')
    logger.info('Removed collective.sidebar Resources')
    p = api.portal
    p.set_registry_record(name='collective.sidebar.root_nav', value=False)  # noqa
    p.set_registry_record(name='collective.sidebar.enable_actions', value=True)  # noqa
    p.set_registry_record(name='collective.sidebar.enable_collapse', value=False)  # noqa
    p.set_registry_record(name='collective.sidebar.enable_cookies', value=False)  # noqa
    logger.info('Added collective.sidebar registry records')
