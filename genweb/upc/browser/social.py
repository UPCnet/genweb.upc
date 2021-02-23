# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.syndication.adapters import FolderFeed, BaseItem
from Products.CMFPlone.interfaces.syndication import IFeedItem

from plone import api
from plone.app.layout.viewlets.common import TitleViewlet
from plone.registry.interfaces import IRegistry

from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.component.hooks import getSite

from genweb.controlpanel.interface import IGenwebControlPanelSettings


class SocialTagsTwitterViewlet(TitleViewlet):

    def get_tags(self):
        site = getSite()
        feed = FolderFeed(site)
        item = queryMultiAdapter((self.context, feed), IFeedItem, default=None)
        if item is None:
            item = BaseItem(self.context, feed)

        registry = getUtility(IRegistry)
        gwsettings = registry.forInterface(IGenwebControlPanelSettings)

        lang = getToolByName(api.portal.get(), 'portal_languages').getPreferredLanguage()
        if not lang:
            lang = 'ca'

        tags = {"site": getattr(gwsettings, 'html_title_{}'.format(lang)),
                "title": item.title,
                "description": item.description,
                "url": item.link,
                "image": None}

        try:
            obj = api.content.find(context=self.context)[0]
            item = obj.getObject()
            has_image = getattr(item, 'image', None)
            if has_image is not None:
                tags["image"] = item.absolute_url() + '/@@images/image'
        except:
            pass

        return tags
