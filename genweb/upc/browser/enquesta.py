# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from five import grok
from hashlib import sha1
from plone import api
from zope.interface import Interface
from zope.interface import alsoProvides

import datetime


class enquestaRedirect(grok.View):
    ## Add new property named 'asepeyo_hash', type string,
    ## in portal_memberdata propierties of plone site 
    ## where you want to run this views.

    grok.name('enquesta')
    grok.context(Interface)
    grok.require('zope2.View')

    def render(self):

        try:
            from plone.protect.interfaces import IDisableCSRFProtection
            alsoProvides(self.request, IDisableCSRFProtection)
        except:
            pass

        context = aq_inner(self.context)
        if api.user.is_anonymous():
            return self.request.response.redirect(context.absolute_url())
        logged_user = api.user.get_current()

        user_token = logged_user.getProperty('asepeyo_hash')
        if not user_token:
            user_seed = '%s %s' % (logged_user.id, datetime.datetime.now().isoformat())
            user_token = sha1(user_seed).hexdigest()
            logged_user.setMemberProperties(mapping={"asepeyo_hash": user_token})

        enquesta_url = 'http://www.encuestafacil.com/RespWeb/Qn.aspx?EID= 2254689&ParamID=%s' % user_token

        return self.request.response.redirect(enquesta_url)


class enquestaTokens(grok.View):
    grok.name('enquesta-tokens')
    grok.context(Interface)
    grok.require('cmf.ManagePortal')

    def render(self):
        mdata = getToolByName(self.context, 'portal_memberdata')
        users = [api.user.get(a) for a in mdata._members]
        users = [user for user in users if user]
        return 'Aquest son els tokens dels usuaris: \n\n'+'\n'.join(['%s,%s' % (user.id, user.getProperty('asepeyo_hash')) for user in users if user.getProperty('asepeyo_hash')])


class enquestaDeleteTokens(grok.View):
    grok.name('enquesta-delete-tokens')
    grok.context(Interface)
    grok.require('cmf.ManagePortal')

    def render(self):
        try:
            from plone.protect.interfaces import IDisableCSRFProtection
            alsoProvides(self.request, IDisableCSRFProtection)
        except:
            pass

        mdata = getToolByName(self.context, 'portal_memberdata')
        users = [api.user.get(a) for a in mdata._members]
        users = [user for user in users if user]

        for user in users:
            if user.getProperty('asepeyo_hash'):
                user.setMemberProperties(mapping={"asepeyo_hash": ''})
        return user.id + ": Poll tokens deleted"
