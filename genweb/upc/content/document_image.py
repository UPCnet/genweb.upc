# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from five import grok
from plone.directives import form
from plone.dexterity.content import Item
from zope.interface import implements


class IDocumentImage(form.Schema):
    """
    """


class DocumentImage(Item):
    implements(IDocumentImage)


class DocumentImageView(grok.View):
    grok.context(IDocumentImage)
    grok.name('view')

    security = ClassSecurityInfo()

    def render(self):
        self.template = ViewPageTemplateFile('document_image_templates/view.pt')
        return self.template(self)
