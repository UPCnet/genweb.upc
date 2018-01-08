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

from genweb.core.adapters import IImportant

from transaction import commit


class TestExample(unittest.TestCase):

    layer = GENWEB_UPC_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def createDefaultDirectories(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        setupview = getMultiAdapter((self.portal, self.request), name='setup-view')
        setupview.apply_default_language_settings()
        setupview.setup_multilingual()
        setupview.createContent('n3')
        commit()
        logout()

    def loginBrowser(self, browser, portalURL):
        browser.open(portalURL + "/login_form")
        browser.getControl(name='__ac_name').value = "admin"
        browser.getControl(name='__ac_password').value = "secret"
        browser.getControl(name='submit').click()

    def openBrowserURL(self, browser, url):
        portalURL = self.portal.absolute_url()
        self.loginBrowser(browser, portalURL)
        browser.open(portalURL + url)

    def testMarkingAsImportantNewsItem(self):
        """ We also created a news to do the test.
        """

        self.createDefaultDirectories()

        login(self.portal, TEST_USER_NAME)
        news_id = 'testnews'
        self.portal.ca.noticies.invokeFactory('News Item', news_id,
            title=u"This is a test")
        self.assertTrue(self.portal.ca.noticies.get(news_id, False))

        news_test = self.portal.ca.noticies.testnews
        IImportant(news_test).is_important = True

        commit()
        logout()

        self.assertTrue(IImportant(news_test).is_important)

        browser = Browser(self.app)
        self.openBrowserURL(browser, "/ca/noticies/folder_contents")

        search_important = ""
        for line in browser.contents.split('\n'):
            if "id=\"folder-contents-item-" + news_id + "\"" in line:
                search_important = line
                break
        self.assertIn("item-important", search_important)

    def testViewListingViewInAEventTypeFolder(self):
        """ Given a event type folder
            When the folder defines a attribute "text"
            Then view does not have to show the value this attribute
        """
        self.createDefaultDirectories()
        login(self.portal, TEST_USER_NAME)
        attributeValue = "missatgeDeProva"
        self.portal.ca.esdeveniments.text = attributeValue
        commit()
        logout()

        browser = Browser(self.app)
        self.openBrowserURL(browser, "/ca/esdeveniments/listing_view")
        self.assertNotIn(attributeValue, browser.contents)
