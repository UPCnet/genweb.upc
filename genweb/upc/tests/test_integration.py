import unittest2 as unittest
from genweb.upc.testing import GENWEB_UPC_INTEGRATION_TESTING
from genweb.upc.testing import GENWEB_UPC_FUNCTIONAL_TESTING
from AccessControl import Unauthorized
from zope.component import getMultiAdapter, queryUtility
from Products.CMFCore.utils import getToolByName

from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles
from plone.app.testing import applyProfile

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from genweb.core.interfaces import IHomePage
from genweb.theme.portlets import homepage

import transaction


class TestExample(unittest.TestCase):

    layer = GENWEB_UPC_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def setup_gw(self):
        portal = self.layer['portal']
        request = self.layer['request']
        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        setupview = getMultiAdapter((portal, request), name='setup-view')
        setupview.setup_multilingual()
        setupview.createContent()

        logout()

    def testSetupViewAvailable(self):
        portal = self.layer['portal']
        self.failUnless(portal.unrestrictedTraverse('@@setup-view'))

    def testSetupViewNotAvailableForAnonymous(self):
        portal = self.layer['portal']
        logout()
        self.assertRaises(Unauthorized, portal.restrictedTraverse, '@@setup-view')

    def testSetupView(self):
        portal = self.layer['portal']
        request = self.layer['request']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        setupview = getMultiAdapter((portal, request), name='setup-view')
        setupview.setup_multilingual()
        setupview.createContent()

        self.assertEqual(portal['en']['news'].Title(), u"News")
        self.assertEqual(portal['es']['banners-es'].Title(), u"Banners")
        self.assertEqual(portal['ca']['logosfooter-ca'].Title(), u"Logos peu")

    def testTemplatesFolderPermissions(self):
        portal = self.layer['portal']
        request = self.layer['request']
        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        setupview = getMultiAdapter((portal, request), name='setup-view')
        setupview.setup_multilingual()
        setupview.createContent()

        logout()
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member', 'Contributor', 'Editor', 'Reader', 'Reviewer'], [])

        # setRoles(portal, 'user1', ['Contributor', 'Editor', 'Reader', 'Reviewer'])
        login(portal, 'user1')
        self.assertRaises(Unauthorized, portal.manage_delObjects, 'templates')

    def testHomePageMarkerInterface(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        setupview = getMultiAdapter((self.portal, self.request), name='setup-view')
        setupview.setup_multilingual()
        setupview.createContent()
        logout()
        self.assertTrue(IHomePage.providedBy(self.portal['ca']['benvingut']))

    # def testFolderConstrains(self):
    #     from genweb.upc.events import CONSTRAINED_TYPES, IMMEDIATELY_ADDABLE_TYPES
    #     from zope.event import notify
    #     from Products.Archetypes.event import ObjectInitializedEvent
    #     setRoles(self.portal, TEST_USER_ID, ['Manager'])
    #     login(self.portal, TEST_USER_NAME)
    #     self.portal.invokeFactory('Folder', 'userfolder', title=u"Soc una carpeta")
    #     folder = self.portal['userfolder']
    #     notify(ObjectInitializedEvent(folder))
    #     self.assertEqual(sorted(folder.getLocallyAllowedTypes()), sorted(CONSTRAINED_TYPES))
    #     self.assertEqual(sorted(folder.getImmediatelyAddableTypes()), sorted(IMMEDIATELY_ADDABLE_TYPES))

    # On the fridge, as the migration worked and is no longer needed
    # def test_rlf_migration(self):
    #     self.setup_gw()
    #     login(self.portal, TEST_USER_NAME)
    #     migration_view = getMultiAdapter((self.portal, self.request), name='migrate_rlf')
    #     migration_view.render()
    #     logout()

    #     self.assertFalse(self.portal.get('ca_old', False))
    #     self.assertFalse(self.portal.get('en_old', False))
    #     self.assertFalse(self.portal.get('es_old', False))

    #     self.assertTrue(self.portal.get('ca', False))
    #     self.assertTrue(self.portal.get('en', False))
    #     self.assertTrue(self.portal.get('es', False))

    #     self.assertTrue(self.portal['ca'].get('benvingut', False))
    #     self.assertTrue(self.portal['ca'].get('shared', False))
