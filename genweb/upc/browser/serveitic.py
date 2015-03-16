# -*- coding: utf-8 -*-
from five import grok

from genweb.theme.browser.interfaces import IGenwebTheme
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _


grok.templatedir("views_templates")


class ServeisTicFolderView(grok.View):
    """ Customize view for Serveis TIC """
    grok.name(_('serveistic_view'))
    grok.context(IFolderish)
    grok.require('zope2.View')
    grok.template('serveitic')
    grok.layer(IGenwebTheme)

    def getTabs(self):
        context = self.context
        pc = getToolByName(context, "portal_catalog")
        tabs = pc.searchResults(portal_type="Document",
                                review_state="published",
                                sort_on="getObjPositionInParent",
                                Subject=('fitxa'),
                                sort_limit=5)
        data = [dict(id=a.pretty_title_or_id,
                     body_tab=a.getObject().text.raw) for a in tabs]
        return data
