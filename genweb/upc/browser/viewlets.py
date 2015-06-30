from five import grok
from plone import api
from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations
from zope.security import checkPermission

from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.app.layout.viewlets.interfaces import IAboveContentTitle
from plone.app.contenttypes.interfaces import IEvent
from plone.app.contenttypes.interfaces import INewsItem

from genweb.core.adapters import IImportant
from genweb.core.interfaces import IGenwebLayer
from genweb.core.interfaces import IHomePage
from genweb.core.utils import portal_url
from genweb.theme.browser.viewlets import viewletBase
from genweb.theme.browser.interfaces import IGenwebTheme
from genweb.upc.browser.interfaces import IGenwebUPC


class notConfigured(grok.Viewlet):
    grok.baseclass()

    def existObjectsNeeded(self):
        """Funcio que mira si existeixen els objectes que son necessaris pel bon funcionament del espai
           TODO: Fer que comprovi mes objectes, per ara nomes comprova la pagina principal en catala
        """
        portal = api.portal.get()
        if not getattr(portal, 'ca', False):
            return False
        return getattr(portal['ca'], 'benvingut', False)

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


class gwSendEvent(viewletBase):
    grok.name('genweb.sendevent')
    grok.context(IEvent)
    grok.template('send_event')
    grok.viewletmanager(IAboveContentTitle)
    grok.layer(IGenwebUPC)

    def isEventSent(self):
        """
        """
        context = self.context
        annotations = IAnnotations(context)
        if 'eventsent' in annotations:
            return True
        else:
            return False

    def canManageSite(self):
        return checkPermission("plone.app.controlpanel.Overview", self.portal())


class gwDontCopy(viewletBase):
    grok.context(IHomePage)
    grok.template('dontcopy')
    grok.viewletmanager(IAboveContentTitle)
    grok.require('cmf.AddPortalContent')
    grok.layer(IGenwebTheme)


class gwImportantNews(viewletBase):
    grok.name('genweb.important')
    grok.context(INewsItem)
    grok.template('important')
    grok.viewletmanager(IAboveContentTitle)
    grok.layer(IGenwebUPC)

    def permisos_important(self):
        # TODO: Comprovar que l'usuari tingui permisos per a marcar com a important
        return not IImportant(self.context).is_important and checkPermission("plone.app.controlpanel.Overview", self.portal())

    def permisos_notimportant(self):
        # TODO: Comprovar que l'usuari tingui permisos per a marcar com a notimportant
        return IImportant(self.context).is_important and checkPermission("plone.app.controlpanel.Overview", self.portal())

    def canManageSite(self):
        return checkPermission("plone.app.controlpanel.Overview", self.portal())

    def isNewImportant(self):
        context = aq_inner(self.context)
        is_important = IImportant(context).is_important
        return is_important
