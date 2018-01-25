import unittest2 as unittest
from genweb.upc.testing import GENWEB_UPC_INTEGRATION_TESTING
from AccessControl import Unauthorized
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles
from genweb.core.interfaces import IHomePage
from genweb.core.adapters import IImportant


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
        setupview.apply_default_language_settings()
        setupview.setup_multilingual()
        setupview.createContent('n3')

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
        setupview.apply_default_language_settings()
        setupview.setup_multilingual()
        setupview.createContent('n3')

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
        setupview.apply_default_language_settings()
        setupview.setup_multilingual()
        setupview.createContent('n3')

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
        setupview.apply_default_language_settings()
        setupview.setup_multilingual()
        setupview.createContent('n3')
        logout()
        self.assertTrue(IHomePage.providedBy(self.portal['ca']['benvingut']))

    def createDefaultDirectories(self):
        """ It would be advisable to use this method in the other classes
        """

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        setupview = getMultiAdapter((self.portal, self.request), name='setup-view')
        setupview.apply_default_language_settings()
        setupview.setup_multilingual()
        setupview.createContent('n3')
        logout()

    def testMarkingAsImportantNewsItem(self):
        """ We also created a news to do the test.
        """

        self.createDefaultDirectories()

        login(self.portal, TEST_USER_NAME)
        news_id = 'testnews'
        self.portal.ca.noticies.invokeFactory('News Item', news_id, title=u"This is a test")
        self.assertTrue(self.portal.ca.noticies.get(news_id, False))

        news_test = self.portal.ca.noticies.testnews
        IImportant(news_test).is_important = True
        logout()

        self.assertTrue(IImportant(news_test).is_important)
