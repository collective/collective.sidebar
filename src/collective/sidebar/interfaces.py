# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveSidebarLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer.
    """

class INavigationEndpoint(Interface):
    """A marker interface for signaling a navigation endpoint.
    """
