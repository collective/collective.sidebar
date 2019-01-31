# -*- coding: utf-8 -*-
"""Init and utils."""
from collective.sidebar.patches import apply_portrait_patch
from zope.i18nmessageid import MessageFactory

import zope.deferredimport


# Patch Profile-Scale
apply_portrait_patch()

# Translation Domain
_ = MessageFactory('collective.sidebar')

# Deferred Imports
zope.deferredimport.defineFrom(
    'collective.sidebar.directives',
    'user_avatar',
    'AVATAR_KEY',
)
