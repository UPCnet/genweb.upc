# -*- coding: utf-8 -*-
from plone.app.contenttypes import _
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implements, alsoProvides
from plone.directives import form


class ICollectionCustom(form.Schema):
    """ """

    logical_op = schema.Choice(
        title=_(u'Operator'),
        description=_(u'Logical operator to refine searches at ZODB'),
        values=['and', 'or'],
        required=False,
        default='or'
    )

alsoProvides(ICollectionCustom, form.IFormFieldProvider)


class CollectionCustom(object):
    implements(ICollectionCustom)

    def __init__(self, context):
        self.context = context

    def _set_logical_op(self, value):
        self.context.logical_op = value

    def _get_logical_op(self):
        return getattr(self.context, 'logical_op', self.context.logical_op)

    logical_op = property(_get_logical_op, _set_logical_op)

    def results(self, batch=True, b_start=0, b_size=None,
                sort_on=None, limit=None, brains=False,
                custom_query={}, logical_op=None):
        querybuilder = getMultiAdapter((self.context, self.context.REQUEST),
                                       name='querybuilderresults')
        sort_order = 'reverse' if self.sort_reversed else 'ascending'
        if not b_size:
            b_size = self.item_count
        if not sort_on:
            sort_on = self.sort_on
        if not limit:
            limit = self.limit
        if not logical_op:
            logical_op = self.logical_op
        query = self.query
        # Handle INavigationRoot awareness as follows:
        # - If query is None or empty then do nothing.
        # - If query already contains a criteria for the index "path", then do
        #   nothing, since plone.app.querybuilder takes care of this
        #   already. (See the code of _path and _relativePath inside
        #   p.a.querystring.queryparser to understand).
        # - If query does not contain any criteria using the index "path", then
        #   add a criteria to match everything under the path "/" (which will
        #   be converted to the actual navigation root path by
        #   p.a.querystring).
        if query:
            has_path_criteria = any(
                (criteria['i'] == 'path')
                for criteria in query
            )
            if not ('k') in query[0]:
                query[0].update({u'k': logical_op})
            if not has_path_criteria:
                # Make a copy of the query to avoid modifying it
                query = list(self.query)
                query.append({
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/',
                })

        return querybuilder(
            query=query, batch=batch, b_start=b_start, b_size=b_size,
            sort_on=sort_on, sort_order=sort_order,
            limit=limit, brains=brains, custom_query=custom_query
        )
