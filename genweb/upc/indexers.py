# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from Products.PlonePAS.utils import safe_unicode

from plone.indexer.decorator import indexer
from plone.app.contenttypes.indexers import _unicode_save_string_concat

from genweb.core.patches import SearchableText
from genweb.upc.content.document_image import IDocumentImage


# Add subjects and creators to searchableText Dexterity objects
# def SearchableText(obj, text=False):
#     subjList = []
#     creatorList = []

#     for sub in obj.subject:
#         subjList.append(sub)
#     subjects = ','.join(subjList)

#     for creator in obj.creators:
#         creatorList.append(creator)
#     creators = ','.join(creatorList)

#     text = ''
#     try:
#         if obj.text and obj.text.output:
#             text = BeautifulSoup(obj.text.output).getText()
#     except:
#         text = ''

#     return u' '.join((
#         safe_unicode(obj.id),
#         safe_unicode(obj.title) or u'',
#         safe_unicode(obj.description) or u'',
#         safe_unicode(subjects) or u'',
#         safe_unicode(creators) or u'',
#         safe_unicode(text) or u'',
#     ))


@indexer(IDocumentImage)
def SearchableText_document_image(obj):
    if obj.text is None or obj.text.output is None:
        return SearchableText(obj)
    return _unicode_save_string_concat(SearchableText(obj), obj.text.output)
