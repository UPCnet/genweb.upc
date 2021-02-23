# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.syndication import IFeedItem
from Products.CMFPlone.browser.syndication.adapters import FolderFeed, BaseItem

from plone import api
from plone.app.layout.viewlets.common import TitleViewlet

from zope.component import queryMultiAdapter
from zope.component.hooks import getSite


class SocialTagsTwitterViewlet(TitleViewlet):

    def get_tags(self):
        site = getSite()
        feed = FolderFeed(site)
        item = queryMultiAdapter((self.context, feed), IFeedItem, default=None)
        if item is None:
            item = BaseItem(self.context, feed)

        tags = {"title": item.title,
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
