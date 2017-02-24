# -*- coding: utf-8 -*-
from zope.interface import implements
from plone import api
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from genweb.core import GenwebMessageFactory as _

from zope import schema
from zope.formlib import form

from pyquery import PyQuery as pq
import re
import requests
from requests.exceptions import RequestException, ReadTimeout
import urlparse


class IContentPortlet(IPortletDataProvider):
    """A portlet which can render an existing content
    """

    ptitle = schema.TextLine(
        title=_(u"Títol del portlet"),
        description=_(u"help_static_content_title_ca"),
        required=True,
        default=_(u"")
    )

    show_title = schema.Bool(
        title=_(u"Mostra el títol?"),
        description=_(u"Marqueu aquesta casella si voleu que es mostri el títol del portlet"),
        required=True,
        default=True,
    )

    hide_footer = schema.Bool(
        title=_(u"Omet el contorn del portlet"),
        description=_(u"Marqueu aquesta casella si es desitja que el text mostrat a dalt sigui visualitzat sense la capçalera, el contorn o el peu estàndard"),
        required=True,
        default=False,
    )

    url = schema.TextLine(
        title=_(u"URL de la pàgina a mostrar"),
        description=_(u"help_static_content_url_ca"),
        required=True
    )

    element = schema.TextLine(
        title=_(u"Element de la pàgina a mostrar, per defecte #content"),
        description=_(u"help_static_content_element_ca"),
        required=True,
        default=_(u"#content")
    )


class Assignment (base.Assignment):
    implements(IContentPortlet)

    def __init__(self, url='http://genweb.upc.edu/ca/demana-un-genweb', ptitle='', element='#content', show_title=True, hide_footer=False):
        # s'invoca quan cliquem a Desa
        # import pdb; pdb.set_trace()
        self.url = url
        self.ptitle = ptitle
        self.element = element
        self.show_title = show_title
        self.hide_footer = hide_footer

    @property
    def title(self):
        return self.ptitle or _(u"Existing Content")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/existing_content.pt')

    def get_catalog_content(self, path_to_search):
        """ Fem una consulta al catalog, en comptes de fer un PyQuery """
        raw_html = u''
        catalog = getToolByName(self.context, 'portal_catalog')
        """ Mirem el cas especial dels form """
        im_searching_forms = catalog(path=path_to_search, object_provides=IPloneFormGenForm.__identifier__)
        if len(im_searching_forms) > 0:
            raw_html = im_searching_forms[0].getObject()()
        else:
            objects = catalog(path=path_to_search)
            try:
                raw_html = objects[0]()
            except:
                raw_html = objects[0].getObject()()
        return raw_html

    def getHTML(self):
        """ Agafa contingut de 'Element' de la 'URL', paràmetres definits per l'usuari
            Avisa si hi ha problemes en la URL o si no troba Element.
        """
        portal_url = getToolByName(self.context, "portal_url")
        portal = portal_url.getPortalObject()
        url_portal_nginx = portal.absolute_url()  # url (per dns) del lloc
        link = self.get_absolute_url(self.data.url)  # url del contingut que vol mostrar l'usuari
        try:
            link_url = re.findall('https?://(.*)', link)[0].strip('/')  # url del contingut netejada
            parent_url = re.findall('https?://(.*)', self.context.absolute_url())[0].strip('/')  # url del pare netejada
            root_url = re.findall('https?://(.*)', url_portal_nginx)[0].strip('/')  # url (per dns) del lloc netejada

            link_a_larrel = link_url.endswith('/ca') or link_url.endswith('/es') or link_url.endswith('/en') == root_url

            if link_url not in parent_url and not link_a_larrel:
                if link_url.startswith(root_url):
                    # link intern, search through the catalog
                    relative_path = re.findall(root_url + '(.*)', link_url)[0]
                    url_to_search = '/'.join(portal.getPhysicalPath()) + relative_path
                    raw_html = self.get_catalog_content(url_to_search)
                    charset = re.findall('charset=(.*)"', raw_html)
                    if len(charset) > 0:
                        clean_html = re.sub(r'[\n\r]?', r'', raw_html.encode(charset[0]))
                        doc = pq(clean_html)
                        match = re.search(r'This page does not exist', clean_html)
                        if not match:
                            content = pq('<div/>').append(
                                doc(self.data.element).outerHtml()).html(method='html')
                            if not content:
                                content = _(u"ERROR. This element does not exist.") + " " + self.data.element
                        else:
                            content = _(u"ERROR: Unknown identifier. This page does not exist." + link)
                    else:
                        content = _(u"ERROR. Charset undefined")
                else:
                    # link extern, pyreq
                    raw_html = requests.get(link, timeout=5)
                    charset = re.findall('charset=(.*)"', raw_html.content)
                    if len(charset) > 0:
                        clean_html = re.sub(r'[\n\r]?', r'', raw_html.content.decode(charset[0]))
                        doc = pq(clean_html)
                        match = re.search(r'This page does not exist', clean_html)
                        if not match:
                            content = pq('<div/>').append(
                                doc(self.data.element).outerHtml()).html(method='html')
                            if not content:
                                content = _(u"ERROR. This element does not exist.") + " " + self.data.element
                        else:
                            content = _(u"ERROR: Unknown identifier. This page does not exist." + link)
                    else:
                        content = _(u"ERROR. Charset undefined")
            else:
                content = _(u"ERROR. Autoreference")
        except ReadTimeout:
            content = _(u"ERROR. There was a timeout while waiting for '{0}'".format(self.get_absolute_url(self.data.url)))
        except RequestException:
            content = _(u"ERROR. This URL does not exist")
        except:
            content = _(u"ERROR. Unexpected exception")
        return content

    def getTitle(self):
        return self.data.ptitle

    def showTitle(self):
        return self.data.show_title

    def getClass(self):
        if self.data.hide_footer:
            return 'existing_content_portlet_no_border'
        else:
            return 'existing_content_portlet'

    def get_absolute_url(self, url):
        """
        Convert relative url to absolute
        """
        if not ("://" in url):
            root = api.portal.get().absolute_url()
            base = root + '/' + api.portal.get_navigation_root(self.context).id + '/'
            return urlparse.urljoin(base, url)
        else:
            # Already absolute
            return url


class AddForm(base.AddForm):
    form_fields = form.Fields(IContentPortlet)
    label = _(u"Afegeix portlet de contingut existent")
    description = _(u"Aquest portlet mostra contingut ja existent en URL específica")

    def create(self, data):
        # s'invoca despres de __init__ en clicar Desa
        assignment = Assignment(**data)
        return assignment


class EditForm(base.EditForm):
    form_fields = form.Fields(IContentPortlet)
    label = _(u"Edita portlet de contingut existent")
    description = _(u"Aquest portlet mostra contingut ja existent en URL específica.")
