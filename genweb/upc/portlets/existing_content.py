#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from genweb.core import GenwebMessageFactory as _

from zope import schema
from zope.formlib import form

from pyquery import PyQuery as pq

import re
import requests
import urlparse
from plone import api


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

    def getHTML(self):
        """ Agafa contingut de 'Element' de la 'URL', paràmetres definits per l'usuari
            Avisa si hi ha problemes en la URL o si no troba Element. 
        """
        try:
            url = self.get_absolute_url(self.data.url)
            # check url to avoid autoreference, removing http(s) and final slash
            check_url = re.findall('https?(.*)\/?', url)[0].strip('/')
            check_parent = re.findall('https?(.*)\/?', self.context.absolute_url())[0].strip('/')
            # check url to avoid reference to root, removing language /xx
            check_root = re.findall('https?(.*)\/?', api.portal.get().absolute_url())[0].strip('/')
            if check_url != check_parent and check_url.strip('/ca').strip('/es').strip('/en') != check_root:
                raw_html = requests.get(url)
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
                        content = _(u"ERROR: Unknown identifier. This page does not exist." + url)
                else:
                    content = _(u"ERROR. Charset undefined")
            else:
                content = _(u"ERROR. Autoreference")
        except requests.exceptions.RequestException:
            content = _(u"ERROR. This URL does not exist.")
        except:
            content = _(u"ERROR. Unexpected exception.")
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
