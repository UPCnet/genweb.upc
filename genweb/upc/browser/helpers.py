from zope.annotation.interfaces import IAnnotations
from plone.portlets.interfaces import IPortletManager, IPortletRetriever
from zope.component import getMultiAdapter, getUtility
from genweb.upc.portlets.existing_content import IContentPortlet

from plone import api
from five import grok
from Products.CMFPlone.interfaces import IPloneSiteRoot

import json

class findPacketbyType(grok.View):
    """ Return all contents of a content type """
    grok.context(IPloneSiteRoot)
    grok.name('find_content_bytype')
    grok.require('cmf.ManagePortal')

    def render(self):
        items = []
        for item in api.content.find(portal_type='packet'):
            item_obj = item.getObject()
            annotations = IAnnotations(item_obj)
            item_type = annotations.get('genweb.packets.type'),
            item_link = annotations.get("genweb.packets.url")
            items.append('{}'.format(dict(where=item.getURL(),
                                          packet_type=item_type,
                                          link=item_link)))
        return items


class findExistingContentPortlets(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('find_existingcontent_portlet')
    grok.require('cmf.ManagePortal')

    def render(self):
        portal = api.portal.get()
        portal_ca = portal['ca']
        portal_en = portal['en']
        portal_es = portal['es']
        portlets_contingut = []
        portlets = ()
        for portal_xx in (portal_ca['benvingut'], portal_en['welcome'], portal_es['bienvenido']):
            for column in ["genweb.portlets.HomePortletManager1",
                           "genweb.portlets.HomePortletManager2",
                           "genweb.portlets.HomePortletManager3",
                           "genweb.portlets.HomePortletManager4",
                           "genweb.portlets.HomePortletManager5",
                           "genweb.portlets.HomePortletManager6",
                           "genweb.portlets.HomePortletManager7",
                           "genweb.portlets.HomePortletManager8",
                           "genweb.portlets.HomePortletManager9",
                           "genweb.portlets.HomePortletManager10"
                           ]:
                            # "plone.leftcolumn",
                            # "plone.rightcolumn"
                manager = getUtility(IPortletManager, name=column, context=portal_xx)
                retriever = getMultiAdapter((portal_xx, manager), IPortletRetriever)
                portlets = retriever.getPortlets()
                if portlets:
                    for portlet in portlets:
                        # portlet is {'category': 'context', 'assignment': <FacebookLikeBoxAssignment at facebook-like-box>, 'name': u'facebook-like-box', 'key': '/isleofback/sisalto/huvit-ja-harrasteet
                        # Identify portlet by interface provided by assignment
                        if IContentPortlet.providedBy(portlet["assignment"]):
                            portlets_contingut.append('{}'.format(dict(where=portal_xx.title,
                                                                       column=column,
                                                                       portlet=portlet["name"],
                                                                       link=portlet["assignment"].url
                                                                       )
                                                                  )
                                                      )
        for item in api.content.find(portal_type='genweb.upc.subhome'):
            item_obj = item.getObject()
            for column in ["genweb.portlets.HomePortletManager1",
                           "genweb.portlets.HomePortletManager2",
                           "genweb.portlets.HomePortletManager3",
                           "genweb.portlets.HomePortletManager4",
                           "genweb.portlets.HomePortletManager5",
                           "genweb.portlets.HomePortletManager6",
                           "genweb.portlets.HomePortletManager7",
                           "genweb.portlets.HomePortletManager8",
                           "genweb.portlets.HomePortletManager9",
                           "genweb.portlets.HomePortletManager10"
                           ]:
                manager = getUtility(IPortletManager, name=column, context=item_obj)
                retriever = getMultiAdapter((item_obj, manager), IPortletRetriever)
                portlets = retriever.getPortlets()
                if portlets:
                    for portlet in portlets:
                        # portlet is {'category': 'context', 'assignment': <FacebookLikeBoxAssignment at facebook-like-box>, 'name': u'facebook-like-box', 'key': '/isleofback/sisalto/huvit-ja-harrasteet
                        # Identify portlet by interface provided by assignment
                        if IContentPortlet.providedBy(portlet["assignment"]):
                            portlets_contingut.append('{}'.format(dict(where=item_obj.title,
                                                                       column=column,
                                                                       portlet=portlet["name"],
                                                                       link=portlet["assignment"].url
                                                                       )
                                                                  )
                                                      )

        if portlets_contingut:
            return portlets_contingut
        else:
            return 'No hi ha portlets'


class replaceElementExistingContentPortlets(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('replace_element_existingcontent_portlet')
    grok.require('cmf.ManagePortal')

    def render(self):
        portlets_error = []
        portlets_found = []
        portlets_not_content = []
        portlets = ()

        pc = api.portal.get_tool('portal_catalog')
        for item in pc.searchResults():
            item_obj = item.getObject()
            for column in ["genweb.portlets.HomePortletManager1",
                           "genweb.portlets.HomePortletManager2",
                           "genweb.portlets.HomePortletManager3",
                           "genweb.portlets.HomePortletManager4",
                           "genweb.portlets.HomePortletManager5",
                           "genweb.portlets.HomePortletManager6",
                           "genweb.portlets.HomePortletManager7",
                           "genweb.portlets.HomePortletManager8",
                           "genweb.portlets.HomePortletManager9",
                           "genweb.portlets.HomePortletManager10",
                           "plone.leftcolumn",
                           "plone.rightcolumn"
                           ]:
                manager = getUtility(IPortletManager, name=column, context=item_obj)
                retriever = getMultiAdapter((item_obj, manager), IPortletRetriever)
                portlets = retriever.getPortlets()
                if portlets:
                    for portlet in portlets:
                        if IContentPortlet.providedBy(portlet["assignment"]):
                            try:
                                if 'element' in self.request.form and portlet['assignment'].element.replace('#', '') == self.request.form['element']:
                                    portlets_found.append(item_obj.absolute_url())

                                    if 'replace' in self.request.form:
                                        portlet['assignment'].element = '#' + self.request.form['replace']

                                if portlet['assignment'].element not in ['#content-core', '#content']:
                                    portlets_not_content.append([portlet['assignment'].element, item_obj.absolute_url()])
                            except:
                                portlets_error.append(item_obj.absolute_url())

        return json.dumps({'changes': portlets_found, 'not_content': portlets_not_content, 'error': portlets_error})