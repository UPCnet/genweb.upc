from plone import api
from plone.portlets.interfaces import IPortletDataProvider
from zope.formlib import form
from zope.interface import implements
from zope import schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.app.portlets import PloneMessageFactory as _
from Acquisition import aq_inner
from Acquisition import aq_parent


class ITagSelectorPortlet(IPortletDataProvider):
    tags = schema.List(title=_(u"Tags"),
                      required=False,
                      value_type=schema.Choice(vocabulary=u'plone.app.vocabularies.Keywords'))


class Assignment (base.Assignment):
    implements(ITagSelectorPortlet)

    def __init__(self, tags):
        self.tags = tags

    @property
    def title(self):
        return _(u"Tag selector")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/tag_selector.pt')

    def update(self):
        # Request parameter
        req = self.request.form
        self.b_start = 'b_start' in req and int(req['b_start']) or 0
        self.b_size = 'b_size' in req and int(req['b_size']) or 10
        self.orphan = 'orphan' in req and int(req['orphan']) or 1
        self.mode = 'mode' in req and req['mode'] or None
        self._date = 'date' in req and req['date'] or None
        self.tags = 'tags' in req and req['tags'] or None
        self.searchable_text = 'SearchableText' in req and\
            req['SearchableText'] or None
        self.path = 'path' in req and req['path'] or None

    def get_tags(self):
        return self.data.tags

    def get_title(self):
        contenttype = self.context.Type()
        if (contenttype in ['Folder', 'Collection']):
            title = self.context.title
        else:
            parent = aq_parent(aq_inner(self.context))
            title = parent.title

        return title

    def tag_url(self, tag=None):
        portal_url = api.portal.get().absolute_url()
        lang = self.context.language
        contenttype = self.context.Type()
        path = self.context.getPhysicalPath()
        if (contenttype in ['Folder', 'Collection']):
            path = path[3:]
        else:
            path = path[3:-1]
        folder_name = "/".join(path)
        if tag:
            return '%s/%s/%s?tags=%s' % (portal_url, lang, folder_name, tag)
        else:
            return '%s/%s/%s' % (portal_url, lang, folder_name)


class AddForm(base.AddForm):
    form_fields = form.Fields(ITagSelectorPortlet)
    description = _(u"This portlet lists tags by type and context.")

    def create(self, data):
        return Assignment(tags=data.get('tags'))


class EditForm(base.EditForm):
    form_fields = form.Fields(ITagSelectorPortlet)
    label = _(u"Edit Tag selector")
    description = _(u"This portlet lists tags by type and context.")
