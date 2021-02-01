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
    api.portal.set_registry_record(name='collective.sidebar.root_nav', value=False)  # noqa
    api.portal.set_registry_record(name='collective.sidebar.enable_actions', value=True)  # noqa
    api.portal.set_registry_record(name='collective.sidebar.enable_collapse', value=False)  # noqa
    api.portal.set_registry_record(name='collective.sidebar.enable_cookies', value=False)  # noqa
    logger.info('Added collective.sidebar registry records')


def to_1300(context):
    context.runAllImportStepsFromProfile('profile-collective.sidebar:to_1300')
    logger.info('Added collective.sidebar registry records')


def to_1400(context):
    context.runAllImportStepsFromProfile('profile-collective.sidebar:to_1400')
    logger.info('Added collective.sidebar registry records')


def to_1500(context):
    context.runAllImportStepsFromProfile('profile-collective.sidebar:to_1500')
    logger.info('Added collective.sidebar registry records')
