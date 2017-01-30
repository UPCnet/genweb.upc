from plone import api
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from plone.app.event.browser.event_view import get_location
from plone.app.layout.navigation.defaultpage import getDefaultPage
from plone.memoize import view

try:
    # from plone.app.collection.interfaces import ICollection
    from plone.app.contenttypes.behaviors.collection import ICollection
except ImportError:
    ICollection = None
try:
    from Products.ATContentTypes.interfaces import IATTopic
except ImportError:
    IATTopic = None


class ListingTagged(BrowserView):

    def __init__(self, context, request):
        super(ListingTagged, self).__init__(context, request)

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

        if self.mode is None:
            self.mode = self._date and 'day' or 'all'

    @property
    def default_context(self):
        # Try to get the default page
        context = self.context
        default = getDefaultPage(context)
        if default:
            context = context[default]
        return context

    @property
    def is_collection(self):
        ctx = self.default_context
        return ICollection and ICollection.providedBy(ctx) or ctx.Type() == 'Collection' or False

    @property
    def is_topic(self):
        ctx = self.default_context
        return IATTopic and IATTopic.providedBy(ctx) or False

    @view.memoize
    def _get_folder_items(self):
        context = self.context
        contenttype = self.context.Type()

        portal = api.portal.get()
        lang = self.context.language
        path = self.context.getPhysicalPath()
        if (contenttype in ['Folder', 'Collection']):
            path = path[3:]
        else:
            path = path[3:-1]

        try:
            folder = portal[lang][path]
        except:
            folder = context

        kw = {}
        kw['path'] = '/'.join(folder.getPhysicalPath())

        if self.tags:
            kw['Subject'] = {'query': self.tags, 'operator': 'and'}

        if self.searchable_text:
            kw['SearchableText'] = self.searchable_text

        kw['sort_on'] = 'getObjPositionInParent'

        cat = getToolByName(context, 'portal_catalog')
        result = cat(**kw)

        return result

    def _get_collection_items(self):
        ctx = self.default_context
        if self.is_collection:
            kw = {}
            kw['batch'] = False
            kw['brains'] = True
            #kw['sort_on'] = 'getObjPositionInParent'
            res = ctx.results(**kw)
            if self.tags:
                res = [x for x in res if self.tags in x.Subject]
        else:
            res = ctx.queryCatalog(batch=False, full_objects=False)
        return res

    def items(self, batch=True):
        res = []
        if self.is_collection or self.is_topic:
            res = self._get_collection_items()
        else:
            res = self._get_folder_items()

        if batch:
            b_start = self.b_start
            b_size = self.b_size
            res = Batch(res, size=b_size, start=b_start, orphan=self.orphan)

        return res

    def set_kw(self, kw):
        if self.tags:
            kw['Subject'] = {'query': self.tags, 'operator': 'and'}

        if self.searchable_text:
            kw['SearchableText'] = self.searchable_text

        kw['sort_on'] = 'getObjPositionInParent'
        return kw

    def batch(self):
        return self.items()

    def get_location(self, occ):
        return get_location(occ)
