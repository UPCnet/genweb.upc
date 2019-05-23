from five import grok
from plone import api
from Acquisition import aq_inner
from OFS.interfaces import IApplication
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.CMFPlone.interfaces import IPloneSiteRoot

from genweb.core.browser.helpers import listPloneSites

class changeCAStoSSO(grok.View):
    """ 
    Change ADAS url prefix to SSO to all Plone instances of this Zope
    """
    grok.context(IApplication)
    grok.name('change_to_SSO')
    grok.require('cmf.ManagePortal')

    def render(self):

        fail_instances = ""
        serverURL = 'https://sso.upc.edu/CAS/'
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        for plonesite in plonesites:
            try:
                plonesite.acl_users.CASUPC.casServerUrlPrefix = serverURL
            except:
                fail_instances += plonesite.id + "\n"

        return "CAS Server URL Prefix changed to SSO in all instances, except:\n" + fail_instances