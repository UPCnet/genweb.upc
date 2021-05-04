# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from five import grok
from plone.app.contenttypes import _
from plone.directives import form
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from zope import schema
from zope.interface import implements

from genweb.core import GenwebMessageFactory as _GwC


class IDocumentImage(form.Schema):
    """
    """
    image = namedfile.NamedBlobImage(
        title=_(u"Lead Image"),
        description=u"",
        required=True,
    )

    not_show_image = schema.Bool(
        title=_GwC(u"not_show_image"),
        description=u"",
        required=False,
    )

    image_caption = schema.TextLine(
        title=_(u"Lead Image Caption"),
        description=u"",
        required=False,
    )


class DocumentImage(Item):
    implements(IDocumentImage)


class DocumentImageView(grok.View):
    grok.context(IDocumentImage)
    grok.name('view')

    security = ClassSecurityInfo()

    def render(self):
        self.template = ViewPageTemplateFile('document_image_templates/view.pt')
        return self.template(self)
