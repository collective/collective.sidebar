# -*- coding: utf-8 -*-

from plone.supermodel.directives import MetadataListDirective
from zope.interface import Interface
from zope.interface.interfaces import IInterface


AVATAR_KEY = u'collective.sidebar.avatar'


class user_avatar(MetadataListDirective):
    """
    Directive used to mark a field as the profile image provider.
    """

    key = AVATAR_KEY
    value = True

    def factory(self, *args):
        """
        The user_avatar directive accepts as arguments one or more
        fieldnames (string) of fields which should be used.
        """
        if not args:
            raise TypeError(
                'The user_avatar directive expects at least one argument.'
            )
        form_interface = Interface
        if IInterface.providedBy(args[0]):
            form_interface = args[0]
            args = args[1:]
        return [(form_interface, field, self.value) for field in args]
