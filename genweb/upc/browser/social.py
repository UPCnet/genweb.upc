# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from plone import api
from plone.app.layout.viewlets.common import TitleViewlet
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from genweb.controlpanel.interface import IGenwebControlPanelSettings


class SocialTagsTwitterViewlet(TitleViewlet):

    def get_tags(self):
        registry = getUtility(IRegistry)
        gwsettings = registry.forInterface(IGenwebControlPanelSettings)

        lang = getToolByName(api.portal.get(), 'portal_languages').getPreferredLanguage()
        if not lang:
            lang = 'ca'

        tags = {"site": getattr(gwsettings, 'html_title_{}'.format(lang)),
                "title": self.context.title,
                "description": self.context.description,
                "url": self.context.absolute_url(),
                "image": None}

        try:
            has_image = getattr(self.context, 'image', None)
            if has_image is not None:
                tags["image"] = self.context.absolute_url() + '/@@images/image'
        except:
            pass

        return tags
