# -*- coding: utf-8 -*-
from plone import api
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.publisher.browser import TestRequest


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('genweb.upc_various.txt') is None:
        return

    portal = getSite()
    view = getMultiAdapter((portal, TestRequest()), name="setupldapupc")
    view.render()

    # Delete the default content types in case that the site got reinstalled
    # from quickinstaller for some reason
    if getattr(portal, 'front-page', False):
        api.content.delete(obj=portal['front-page'])
    if getattr(portal, 'news', False):
        api.content.delete(obj=portal['news'])
    if getattr(portal, 'events', False):
        api.content.delete(obj=portal['events'])
    if getattr(portal, 'Members', False):
        api.content.delete(obj=portal['Members'])
