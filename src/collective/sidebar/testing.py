# -*- coding: utf-8 -*-

from Acquisition import aq_get
from collective.sidebar.interfaces import ICollectiveSidebarLayer
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing import z2
from zope.interface import alsoProvides

import collective.sidebar


def set_browserlayer(request):
    """
    Set the BrowserLayer for the request.
    We have to set the browserlayer manually, since importing the profile alone
    doesn't do it in tests.
    """
    alsoProvides(request, ICollectiveSidebarLayer)


def setup_sdm(portal):
    """
    Setup session data manager.
    """
    tf_name = 'temp_folder'
    idmgr_name = 'browser_id_manager'
    toc_name = 'temp_transient_container'
    sdm_name = 'session_data_manager'

    from Products.Sessions.BrowserIdManager import BrowserIdManager
    from Products.Sessions.SessionDataManager import SessionDataManager
    from Products.TemporaryFolder.TemporaryFolder import MountedTemporaryFolder
    from Products.Transience.Transience import TransientObjectContainer
    import transaction

    bidmgr = BrowserIdManager(idmgr_name)
    tf = MountedTemporaryFolder(tf_name, title='Temporary Folder')
    toc = TransientObjectContainer(
        toc_name,
        title='Temporary Transient Object Container',
        timeout_mins=20,
    )
    session_data_manager = SessionDataManager(
        id=sdm_name,
        path=tf_name + '/' + toc_name,
        title='Session Data Manager',
        requestName='TESTOFSESSION',
    )
    portal._setObject(idmgr_name, bidmgr)
    portal._setObject(sdm_name, session_data_manager)
    portal._setObject(tf_name, tf)
    portal.temp_folder._setObject(toc_name, toc)
    transaction.commit()


class CollectiveSidebarLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        request = aq_get(app, 'REQUEST')
        request.environ['HTTP_ACCEPT_LANGUAGE'] = 'de'
        self.loadZCML(package=collective.sidebar)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.sidebar:default')
        portal.acl_users.userFolderAddUser(
            SITE_OWNER_NAME,
            SITE_OWNER_PASSWORD,
            ['Manager'],
            [],
        )


class CollectiveSidebarTestingLayer(CollectiveSidebarLayer):
    def setUpPloneSite(self, portal):  # noqa
        applyProfile(portal, 'collective.sidebar:testing')
        portal.acl_users.userFolderAddUser(
            SITE_OWNER_NAME,
            SITE_OWNER_PASSWORD,
            ['Manager'],
            [],
        )


class CollectiveSidebarSessionLayer(CollectiveSidebarTestingLayer):
    def setUpPloneSite(self, portal):
        super(CollectiveSidebarSessionLayer, self).setUpPloneSite(portal)
        setup_sdm(portal)


COLLECTIVE_SIDEBAR_FIXTURE = CollectiveSidebarLayer()
COLLECTIVE_SIDEBAR_TESTING_FIXTURE = CollectiveSidebarTestingLayer()
COLLECTIVE_SIDEBAR_ACCEPTANCE_SESSION_FIXTURE = CollectiveSidebarSessionLayer()

COLLECTIVE_SIDEBAR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SIDEBAR_TESTING_FIXTURE,),
    name='CollectiveSidebarLayer:IntegrationTesting',
)


COLLECTIVE_SIDEBAR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_SIDEBAR_TESTING_FIXTURE,),
    name='CollectiveSidebarLayer:FunctionalTesting',
)


COLLECTIVE_SIDEBAR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_SIDEBAR_ACCEPTANCE_SESSION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveSidebarLayer:AcceptanceTesting',
)
