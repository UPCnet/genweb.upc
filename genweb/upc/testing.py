from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import genweb.upc


GENWEB_UPC = PloneWithPackageLayer(
    zcml_package=genweb.upc,
    zcml_filename='testing.zcml',
    gs_profile_id='genweb.upc:testing',
    name="GENWEB_UPC")

GENWEB_UPC_INTEGRATION = IntegrationTesting(
    bases=(GENWEB_UPC, ),
    name="GENWEB_UPC_INTEGRATION")

GENWEB_UPC_FUNCTIONAL = FunctionalTesting(
    bases=(GENWEB_UPC, ),
    name="GENWEB_UPC_FUNCTIONAL")
