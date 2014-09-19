from five import grok
from Acquisition import aq_inner

from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.layout.viewlets.interfaces import IAboveContent

from genweb.core.interfaces import IGenwebLayer
from genweb.core.interfaces import IHomePage
from genweb.core.utils import portal_url


class notConfigured(grok.Viewlet):
    grok.baseclass()

    def existObjectsNeeded(self):
        """Funcio que mira si existeixen els objectes que son necessaris pel bon funcionament del espai
           TODO: Fer que comprovi mes objectes, per ara nomes comprova la pagina principal en catala
        """
        context = aq_inner(self.context)
        if not getattr(context, 'ca', False):
            return False
        return getattr(context['ca'], 'benvingut', False)

    def getSetupLink(self):
        """Funcio que dona l'enllas al formulari de creacio dels elements per defecte
        """
        return portal_url() + "/setup-view"


class notConfiguredForHomes(notConfigured):
    grok.viewletmanager(IAboveContent)
    grok.context(IHomePage)
    grok.template('notconfigured')
    grok.require('cmf.ManagePortal')
    grok.layer(IGenwebLayer)


class notConfiguredForRoots(notConfigured):
    grok.viewletmanager(IAboveContent)
    grok.context(IPloneSiteRoot)
    grok.template('notconfigured')
    grok.require('cmf.ManagePortal')
    grok.layer(IGenwebLayer)
