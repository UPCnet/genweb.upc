from zope.configuration import xmlconfig

from plone.testing import z2
#from plone.testing.z2 import ZSERVER_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class GenwebUPC(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import genweb.upc
        xmlconfig.file('configure.zcml',
                       genweb.upc,
                       context=configurationContext)

        xmlconfig.file('testing.zcml',
                       genweb.upc.tests,
                       context=configurationContext)

        # Install archetypes-based products
        # z2.installProduct(app, 'upc.genweb.banners')
        z2.installProduct(app, 'upc.genweb.logosfooter')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        # applyProfile(portal, 'genweb.upc:default')
        applyProfile(portal, 'genweb.upc.tests:testing')

    def tearDownZope(self, app):
        # Uninstall archetypes-based products
        z2.uninstallProduct(app, 'upc.genweb.banners')
        z2.uninstallProduct(app, 'upc.genweb.logosfooter')


GENWEB_UPC_FIXTURE = GenwebUPC()
GENWEB_UPC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEB_UPC_FIXTURE,),
    name="GenwebUPC:Integration")
GENWEB_UPC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEB_UPC_FIXTURE,),
    name="GenwebUPC:Functional")
