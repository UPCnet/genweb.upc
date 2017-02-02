# -*- coding: utf-8 -*-

import random

from zope.interface import implements
from zope.component import getMultiAdapter, getUtility
from zope import schema
from zope.formlib import form
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.i18n.normalizer.interfaces import IIDNormalizer

from AccessControl import getSecurityManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from genweb.core import GenwebMessageFactory as _


VIEW_TYPE_LIST = 'list'
VIEW_TYPE_IMG_LEFT_TITLE_RIGHT = 'img_left_title_right'
VIEW_TYPE_IMG_UP_TITLE_DOWN = 'img_up_title_down'
VIEW_TYPE_IMG_UP_TITLE_DOWN_2COLUMNS = 'img_up_title_down_2columns'

vocabulary_view_type = SimpleVocabulary([
    SimpleTerm(
        value=VIEW_TYPE_LIST,
        title=_(u'List view')),
    SimpleTerm(
        value=VIEW_TYPE_IMG_LEFT_TITLE_RIGHT,
        title=_(u'Normal view')),
    SimpleTerm(
        value=VIEW_TYPE_IMG_UP_TITLE_DOWN,
        title=_(u'Full view')),
    SimpleTerm(
        value=VIEW_TYPE_IMG_UP_TITLE_DOWN_2COLUMNS,
        title=_(u'Full2cols view'))])


class IMultiviewCollectionPortlet(IPortletDataProvider):
    """
    Renders a collection in multiple ways.
    """
    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    target_collection = schema.Choice(
        title=_(u"Target collection"),
        description=_(u"Find the collection which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Specify the maximum number of items to show in the "
                      u"portlet. Leave this blank to show all items."),
        required=False)

    random = schema.Bool(
        title=_(u"Select random items"),
        description=_(u"If enabled, items will be selected randomly from the "
                      u"collection, rather than based on its sort order."),
        required=True,
        default=False)

    show_more = schema.Bool(
        title=_(u"Show more... link"),
        description=_(u"If enabled, a more... link will appear in the footer "
                      u"of the portlet, linking to the underlying "
                      u"Collection."),
        required=True,
        default=True)

    show_dates = schema.Bool(
        title=_(u"Show dates"),
        description=_(u"If enabled, effective dates will be shown underneath "
                      u"the items listed."),
        required=True,
        default=False)

    exclude_context = schema.Bool(
        title=_(u"Exclude the Current Context"),
        description=_(
            u"If enabled, the listing will not include the current item the "
            u"portlet is rendered for if it otherwise would be."),
        required=True,
        default=True)

    view_type = schema.Choice(
        title=_(u'View type'),
        description=_(u'Choose how the portlet must be rendered'),
        required=True,
        vocabulary=vocabulary_view_type,
        default=VIEW_TYPE_LIST)


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMultiviewCollectionPortlet)

    header = u""
    target_collection = None
    limit = None
    random = False
    show_more = True
    show_dates = False
    exclude_context = False
    view_type = VIEW_TYPE_LIST

    def __init__(self, header=u"", target_collection=None, limit=None,
                 random=False, show_more=True, show_dates=False,
                 exclude_context=True, view_type=VIEW_TYPE_LIST):
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.random = random
        self.show_more = show_more
        self.show_dates = show_dates
        self.exclude_context = exclude_context
        self.view_type = view_type

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):

    TEMPLATE_FOLDER = 'templates'
    TEMPLATE_FILE = {
        VIEW_TYPE_LIST: 'list.pt',
        VIEW_TYPE_IMG_LEFT_TITLE_RIGHT: 'img_left_title_right.pt',
        VIEW_TYPE_IMG_UP_TITLE_DOWN: 'img_up_title_down.pt',
        VIEW_TYPE_IMG_UP_TITLE_DOWN_2COLUMNS: 'img_up_title_down_2columns.pt',
    }
    SUMMARY_LENGTH_MAX = 200

    def render(self):
        view_type = getattr(self.data, 'view_type', VIEW_TYPE_LIST)
        return ViewPageTemplateFile('{folder}/{file}'.format(
            folder=Renderer.TEMPLATE_FOLDER,
            file=Renderer.TEMPLATE_FILE[view_type]))(self)

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @property
    def available(self):
        return len(self.results())

    def show_time(self):
        return self.data.show_dates

    def more_info(self):
        return self.data.show_more

    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return None
        else:
            return collection.absolute_url()

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portlet-collection-%s" % normalizer.normalize(header)

    def result_dicts_columns(self):
        """
        Return a tuple with (even, odd) dictionaries of results.
        """
        result_dicts = self.result_dicts()
        return (
            dict(div_id="pair-news", results=result_dicts[0::2]),
            dict(div_id="odd-news", results=result_dicts[1::2]))

    def result_dicts(self):
        """
        Transform results into dictionaries of results containing only the data
        to render from templates.
        """
        result_dicts = []
        for result in self.results():
            result_obj = result.getObject()
            result_image = getattr(result_obj, 'image', None)
            try:
                result_description = result.description
            except:
                try:
                    result_description = result.Description()
                except:
                    result_description = ''
            result_dicts.append(dict(
                date=result.EffectiveDate(),
                description=self._summarize(result_description),
                image=result_image,
                image_caption=getattr(result_obj, 'image_caption', None),
                image_src=("{0}/@@images/image/mini".format(result.getURL())
                           if result_image else None),
                title=result.title,
                url=result.getURL(),
            ))
        return result_dicts

    def _summarize(self, text):
        summary = text
        if len(summary) > Renderer.SUMMARY_LENGTH_MAX:
            summary = text[:Renderer.SUMMARY_LENGTH_MAX]
            last_space = summary.rfind(' ')
            last_space = -3 if last_space == -1 else last_space
            summary = summary[:last_space] + '...'
        return summary

    @memoize
    def results(self):
        if self.data.random:
            return self._random_results()
        else:
            return self._standard_results()

    def _standard_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            context_path = '/'.join(self.context.getPhysicalPath())
            exclude_context = getattr(self.data, 'exclude_context', False)
            limit = self.data.limit
            if limit and limit > 0:
                # pass on batching hints to the catalog
                results = collection.queryCatalog(
                    batch=True, b_size=limit + exclude_context)
                results = results._sequence
            else:
                results = collection.queryCatalog()
            if exclude_context:
                results = [
                    brain for brain in results
                    if brain.getPath() != context_path]
            if limit and limit > 0:
                results = results[:limit]
        return results

    def _random_results(self):
        # intentionally non-memoized
        results = []
        collection = self.collection()
        if collection is not None:
            context_path = '/'.join(self.context.getPhysicalPath())
            exclude_context = getattr(self.data, 'exclude_context', False)
            results = collection.queryCatalog(sort_on=None)
            if results is None:
                return []
            limit = self.data.limit and min(len(results), self.data.limit) or 1

            if exclude_context:
                results = [
                    brain for brain in results
                    if brain.getPath() != context_path]
            if len(results) < limit:
                limit = len(results)
            results = random.sample(results, limit)

        return results

    @memoize
    def collection(self):
        collection_path = self.data.target_collection
        if not collection_path:
            return None

        if collection_path.startswith('/'):
            collection_path = collection_path[1:]

        if not collection_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(collection_path, unicode):
            # restrictedTraverse accepts only strings
            collection_path = str(collection_path)

        result = portal.unrestrictedTraverse(collection_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result

    def include_empty_footer(self):
        """
        Whether or not to include an empty footer element when the more
        link is turned off.
        Always returns True (this method provides a hook for
        sub-classes to override the default behaviour).
        """
        return True


class AddForm(base.AddForm):

    form_fields = form.Fields(IMultiviewCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Add Multi-view Collection Portlet")
    description = _(u"This portlet displays a listing of items from a "
                    u"Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IMultiviewCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Edit Multi-view Collection Portlet")
    description = _(u"This portlet displays a listing of items from a "
                    u"Collection.")
