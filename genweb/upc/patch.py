import logging

from zope.component import getUtilitiesFor

from zope.i18nmessageid import MessageFactory

from plone.app.contentlisting.interfaces import IContentListing
from plone.app.querystring import queryparser
from plone.app.querystring.interfaces import IParsedQueryIndexModifier

from Products.CMFCore.utils import getToolByName
from plone.batching import Batch
from plone.memoize.instance import memoize

from genweb.core.utils import pref_lang


logger = logging.getLogger('plone.app.querystring')
_ = MessageFactory('plone')


def __call__(self, query, batch=False, b_start=0, b_size=30,
             sort_on=None, sort_order=None, limit=0, brains=False,
             custom_query=None):
    """If there are results, make the query and return the results"""
    if self._results is None:
        try:
            op = query[0]['k']
            if op == 'undefined':
                op = self.context.logical_op
        except:
            try:
                op = self.context.logical_op
            except:
                op = 'or'
        self._results = self._makequery(
            query=query,
            batch=batch,
            b_start=b_start,
            b_size=b_size,
            sort_on=sort_on,
            sort_order=sort_order,
            limit=limit,
            brains=brains,
            custom_query=custom_query,
            logical_op=op)

    return self._results


def _makequery(self, query=None, batch=False, b_start=0, b_size=30,
               sort_on=None, sort_order=None, limit=0, brains=False,
               custom_query=None, logical_op=None):
    """Parse the (form)query and return using multi-adapter"""
    parsedquery = queryparser.parseFormquery(
        self.context, query, sort_on, sort_order)

    index_modifiers = getUtilitiesFor(IParsedQueryIndexModifier)
    for name, modifier in index_modifiers:
        if name in parsedquery:
            new_name, query = modifier(parsedquery[name])
            parsedquery[name] = query
            # if a new index name has been returned, we need to replace
            # the native ones
            if name != new_name:
                del parsedquery[name]
                parsedquery[new_name] = query

    # Check for valid indexes
    catalog = getToolByName(self.context, 'portal_catalog')
    valid_indexes = [index for index in parsedquery
                     if index in catalog.indexes()]

    # We'll ignore any invalid index, but will return an empty set if none
    # of the indexes are valid.
    if not valid_indexes:
        logger.warning(
            "Using empty query because there are no valid indexes used.")
        parsedquery = {}

    if not parsedquery:
        if brains:
            return []
        else:
            return IContentListing([])

    if batch:
        parsedquery['b_start'] = b_start
        parsedquery['b_size'] = b_size
    elif limit:
        parsedquery['sort_limit'] = limit

    if 'path' not in parsedquery:
        parsedquery['path'] = {'query': ''}

    if isinstance(custom_query, dict):
        # Update the parsed query with extra query dictionary. This may
        # override parsed query options.
        parsedquery.update(custom_query)

    if 'Subject' in parsedquery:
        pq = parsedquery
        pq['Subject'] = {'query': query['query'], 'operator': logical_op}

    results = catalog(**parsedquery)

    if getattr(results, 'actual_result_count', False) and limit\
            and results.actual_result_count > limit:
        results.actual_result_count = limit

    if not brains:
        results = IContentListing(results)
    if batch:
        results = Batch(results, b_size, start=b_start)
    return results


@memoize
def plone_app_portlets_recent_data(self):
    limit = self.data.count
    path = self.navigation_root_path
    portal_type = list(self.typesToShow)
    try:
        portal_type.remove('Image')
    except ValueError:
        pass
    return self.catalog(
        portal_type=portal_type,
        path=path,
        sort_on='modified',
        sort_order='reverse',
        sort_limit=limit)[:limit]
