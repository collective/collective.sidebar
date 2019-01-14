# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return ['collective.sidebar:uninstall']


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def testing(context):
    """post_handler for the collective.sidebar:testing profile"""
    # Do something at the end of the testing installation of this package.
    api.user.create(
        email='max.mustermann@testing.com',
        username='mmustermann',
        password='testing@collective.sidebar123',
        properties={
            'fullname': u'Max Mustermann',
        },
    )
