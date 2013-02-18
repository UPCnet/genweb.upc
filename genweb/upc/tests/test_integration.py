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
        # self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    # def test_product_is_installed(self):
    #     """ Validate that our products GS profile has been run and the product
    #         installed
    #     """
    #     pid = 'genweb.upc'
    #     installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
    #     self.assertTrue(pid in installed,
    #                     'package appears not to have been installed')

    def testSetupViewAvailable(self):
        portal = self.layer['portal']
        self.failUnless(portal.unrestrictedTraverse('@@setup-view'))

    def testSetupViewNotAvailableForAnonymous(self):
        portal = self.layer['portal']
        self.assertRaises(Unauthorized, portal.restrictedTraverse, '@@setup-view')

    def testSetupView(self):
        portal = self.layer['portal']
        request = self.layer['request']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        setupview = getMultiAdapter((portal, request), name='setup-view')
        setupview.createContent()
        self.assertEqual(portal['news'].Title(), u"News")
        self.assertEqual(portal['banners-es'].Title(), u"Banners")
        self.assertEqual(portal['logosfooter-ca'].Title(), u"Logos peu")

    def testTemplatesFolderPermissions(self):
        portal = self.layer['portal']
        request = self.layer['request']
        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        setupview = getMultiAdapter((portal, request), name='setup-view')
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
        setupview.createContent()
        logout()
        self.assertTrue(IHomePage.providedBy(self.portal['benvingut']))

    def testFolderConstrains(self):
        from genweb.upc.events import CONSTRAINED_TYPES, IMMEDIATELY_ADDABLE_TYPES
        from zope.event import notify
        from Products.Archetypes.event import ObjectInitializedEvent
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Folder', 'userfolder', title=u"Soc una carpeta")
        folder = self.portal['userfolder']
        notify(ObjectInitializedEvent(folder))
        self.assertEqual(sorted(folder.getLocallyAllowedTypes()), sorted(CONSTRAINED_TYPES))
        self.assertEqual(sorted(folder.getImmediatelyAddableTypes()), sorted(IMMEDIATELY_ADDABLE_TYPES))
