# -*- coding: utf-8 -*-
from cgi import escape
from five import grok
from plone import api
from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations
from zope.interface import Interface
from zope.security import checkPermission
from zope.component import getMultiAdapter

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.viewlets.interfaces import IHtmlHead
from plone.app.layout.viewlets.common import TitleViewlet, ManagePortletsFallbackViewlet
from plone.app.layout.viewlets.interfaces import IAboveContent, IAboveContentTitle, IBelowContent
from plone.app.contenttypes.interfaces import IEvent
from plone.app.contenttypes.interfaces import INewsItem

from genweb.core.adapters import IImportant
from genweb.core.interfaces import IGenwebLayer
from genweb.core.interfaces import IHomePage
from genweb.core.utils import portal_url
from genweb.theme.browser.viewlets import viewletBase
from genweb.theme.browser.interfaces import IGenwebTheme
from genweb.upc.browser.interfaces import IGenwebUPC
from genweb.upc.content.subhome import ISubhome

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName
from genweb.core.utils import pref_lang
from AccessControl import getSecurityManager

import re

from genweb.theme.browser.viewlets import gwHeader as gwh
from genweb.theme.browser.viewlets import gwFooter as gwf


class gwHeader(gwh):
    grok.layer(IGenwebUPC)
    grok.template('header')


class gwFooter(gwf):
    grok.layer(IGenwebUPC)
    grok.template('footer')


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
    grok.require('cmf.ModifyPortalContent')
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
    grok.require('cmf.ModifyPortalContent')
    grok.layer(IGenwebUPC)

    def permisos_important(self):
        # TODO: Comprovar que l'usuari tingui permisos per a marcar com a important
        return not IImportant(self.context).is_important and checkPermission("plone.app.controlpanel.Overview", self.portal())

    def permisos_notimportant(self):
        # TODO: Comprovar que l'usuari tingui permisos per a marcar com a notimportant
        return IImportant(self.context).is_important and checkPermission("plone.app.controlpanel.Overview", self.portal())

    def isNewImportant(self):
        context = aq_inner(self.context)
        is_important = IImportant(context).is_important
        return is_important


class socialtoolsViewlet(viewletBase):
    grok.name('genweb.socialtools')
    grok.template('socialtools')
    grok.viewletmanager(IAboveContentTitle)
    grok.layer(IGenwebUPC)

    def getData(self):
        Title = aq_inner(self.context).Title()
        contextURL = self.context.absolute_url()

        return dict(Title=Title, URL=contextURL)

    def is_social_tools_enabled(self):
        return not self.genweb_config().treu_icones_xarxes_socials


class gwTitleViewlet(TitleViewlet, viewletBase):
    grok.context(Interface)
    grok.name('plone.htmlhead.title')
    grok.viewletmanager(IHtmlHead)
    grok.layer(IGenwebUPC)

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        page_title = escape(safe_unicode(context_state.object_title()))
        portal_title = escape(safe_unicode(portal_state.navigation_root_title()))

        # Mixed with SEO Properties
        # try:
        #     self.seo_context = getMultiAdapter((self.context, self.request), name=u'seo_context')

        #     self.override_title = self.seo_context['has_seo_title']
        #     self.has_comments = self.seo_context['has_html_comment']
        #     self.has_noframes = self.seo_context['has_noframes']
        # except:
        #     self.override_title = False
        #     self.has_comments = False
        #     self.has_noframes = False

        # if self.override_title:
        #     genweb_title = u'%s' % escape(safe_unicode(self.seo_context['seo_title']))
        # else:
        genweb_title = getattr(self.genweb_config(), 'html_title_%s' % self.pref_lang(), 'Genweb UPC')

        if not genweb_title:
            genweb_title = 'Genweb UPC'
        genweb_title = escape(safe_unicode(re.sub(r'(<.*?>)', r'', genweb_title)))

        marca_UPC = escape(safe_unicode(u"UPC. Universitat Politècnica de Catalunya"))

        if page_title == portal_title:
            self.site_title = u"%s &mdash; %s" % (genweb_title, marca_UPC)
        else:
            self.site_title = u"%s &mdash; %s &mdash; %s" % (page_title, genweb_title, marca_UPC)


class gwManagePortletsFallbackViewletMixin(object):
    """ The override for the manage_portlets_fallback viewlet for IPloneSiteRoot
    """

    render = ViewPageTemplateFile('viewlets_templates/manage_portlets_fallback.pt')

    def getPortletContainerPath(self):
        context = aq_inner(self.context)

        container_url = context.absolute_url()

        # Portlet container will be in the context,
        # Except in the portal root, when we look for an alternative
        if INavigationRoot.providedBy(self.context):
            pc = getToolByName(context, 'portal_catalog')
            # Add the use case of mixin types of IHomepages. The main ones of a
            # non PAM-enabled site and the possible inner ones.
            result = pc.searchResults(object_provides=IHomePage.__identifier__,
                                      portal_type='Document',
                                      Language=pref_lang())

            if result:
                # Return the object without forcing a getObject()
                container_url = result[0].getURL()

        return container_url

    def managePortletsURL(self):
        return "%s/%s" % (self.getPortletContainerPath(), '@@manage-homeportlets')

    def manageSubhomePortletsURL(self):
        return "%s/%s" % (self.getPortletContainerPath(), '@@manage-subhome')

    def available(self):
        secman = getSecurityManager()

        if secman.checkPermission('Genweb: Manage home portlets', self.context):
            return True
        else:
            return False

    def canManageGrid(self):
        secman = getSecurityManager()
        user = secman.getUser()
        context = self.context
        roles = user.getRolesInContext(context)
        if 'Author' in roles or 'Owner' in roles or 'Editor' in roles or 'Contributor' in roles or 'Manager' in roles or 'Reviewer' in roles or 'Site Administrator' in roles or 'WebMaster' in roles:
            return True
        # Reader or Authenticated or Member
        else:
            return False


class gwManagePortletsFallbackViewletForIHomePage(gwManagePortletsFallbackViewletMixin, ManagePortletsFallbackViewlet, viewletBase):
    """ The override for the manage_portlets_fallback viewlet for ISubhome
    """
    grok.context(ISubhome)
    grok.name('plone.manage_portlets_fallback')
    grok.viewletmanager(IBelowContent)
    grok.layer(IGenwebUPC)
