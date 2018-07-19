# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.sidebar


class CollectiveSidebarLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.sidebar)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.sidebar:default')


COLLECTIVE_SIDEBAR_FIXTURE = CollectiveSidebarLayer()


COLLECTIVE_SIDEBAR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SIDEBAR_FIXTURE,),
    name='CollectiveSidebarLayer:IntegrationTesting',
)


COLLECTIVE_SIDEBAR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_SIDEBAR_FIXTURE,),
    name='CollectiveSidebarLayer:FunctionalTesting',
)


COLLECTIVE_SIDEBAR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_SIDEBAR_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveSidebarLayer:AcceptanceTesting',
)
