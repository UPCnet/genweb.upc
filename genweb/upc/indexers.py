# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from plone.app.contenttypes.indexers import _unicode_save_string_concat

from genweb.core.patches import SearchableText
from genweb.upc.content.document_image import IDocumentImage


@indexer(IDocumentImage)
def SearchableText_document_image(obj):
    if obj.text is None or obj.text.output is None:
        return SearchableText(obj)
    return _unicode_save_string_concat(SearchableText(obj), obj.text.output)
