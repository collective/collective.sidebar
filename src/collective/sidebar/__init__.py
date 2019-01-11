# -*- coding: utf-8 -*-
"""Init and utils."""
from collective.sidebar.patches import apply_portrait_patch
from zope.i18nmessageid import MessageFactory


apply_portrait_patch()
_ = MessageFactory('collective.sidebar')
