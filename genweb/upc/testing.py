from zope.configuration import xmlconfig

from plone.testing import z2
#from plone.testing.z2 import ZSERVER_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.app.multilingual.testing import SESSIONS_FIXTURE

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE


class GenwebUPC(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, SESSIONS_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import genweb.upc
        xmlconfig.file('configure.zcml',
                       genweb.upc,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # Needed for PAC not complain about not having one... T_T
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")

        # Install into Plone site using portal_setup
        applyProfile(portal, 'genweb.upc:default')

GENWEB_UPC_FIXTURE = GenwebUPC()
GENWEB_UPC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEB_UPC_FIXTURE,),
    name="GenwebUPC:Integration")
GENWEB_UPC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEB_UPC_FIXTURE,),
    name="GenwebUPC:Functional")
