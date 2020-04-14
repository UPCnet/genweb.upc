# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from pyquery import PyQuery as pq
from requests.exceptions import ReadTimeout
from requests.exceptions import RequestException
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import Invalid
from zope.interface import implements
from zope.interface import invariant
from zope.site import hooks

from genweb.core import GenwebMessageFactory as _

import DateTime
import re
import requests


class NotAnExternalLink(schema.ValidationError):
    __doc__ = _(u"This is an inner link")

# Define a validation method for external URL


def validate_externalurl(value):
    root_url = hooks.getSite().absolute_url()
    link_extern = value.lower()

    if root_url.startswith("http://"):
        root_url = root_url[7:]
    elif root_url.startswith("https://"):
        root_url = root_url[8:]

    if link_extern.startswith("http://"):
        link_extern = link_extern[7:]
    elif link_extern.startswith("https://"):
        link_extern = link_extern[8:]

    isInnerLink = link_extern.startswith(root_url)
    if isInnerLink:
        raise NotAnExternalLink(value)
    return not isInnerLink


class INewContentPortlet(IPortletDataProvider):
    """A portlet which can render an existing content
    """

    ptitle = schema.TextLine(
        title=_(u"Títol del portlet"),
        description=_(u"help_static_content_title_ca"),
        required=False,
        default=_(u"")
    )

    show_title = schema.Bool(
        title=_(u"Mostra el títol?"),
        description=_(u"Marqueu aquesta casella si voleu que es mostri el títol del portlet"),
        required=False,
        default=True,
    )

    hide_footer = schema.Bool(
        title=_(u"Omet el contorn del portlet"),
        description=_(u"Marqueu aquesta casella si es desitja que el text mostrat a dalt sigui visualitzat sense la capçalera, el contorn o el peu estàndard"),
        required=False,
        default=False,
    )

    content_or_url = schema.Choice(
        title=(u"Tipus de contingut"),
        description=(u"Escull el tipus de contingut que vols"),
        required=True,
        values=['EXTERN', 'INTERN']
    )

    external_url = schema.URI(
        title=_(u"EXTERN: URL de la pàgina a mostrar"),
        description=_(u"help_static_content_url_ca"),
        required=False,
        constraint=validate_externalurl,
    )

    own_content = schema.Choice(
        title=_(u"INTERN: Existing content", default=u"INTERN: Existing content"),
        description=_(u'help_existing_content', default=u"You may search for and choose an existing content"),
        required=False,
        source=SearchableTextSourceBinder({}, default_query='path:')
    )

    element = schema.TextLine(
        title=_(u"Element de la pàgina a mostrar, per defecte #content-core"),
        description=_(u"help_static_content_element_ca"),
        required=True,
        default=_(u"#content-core")
    )

    @invariant
    def validate_isFull(data):
        if data.content_or_url == 'INTERN' and not data.own_content:
            raise Invalid(_(u"Falta seleccionar el contingut intern"))
        elif data.content_or_url == 'EXTERN' and not data.external_url:
            raise Invalid(_(u"Falta l'enllaç extern"))


class Assignment (base.Assignment):
    implements(INewContentPortlet)

    def __init__(self, content_or_url, external_url, ptitle, own_content, element='#content-core', show_title=True, hide_footer=False):
        # s'invoca quan cliquem a Desa
        # import pdb; pdb.set_trace()

        self.ptitle = ptitle
        self.show_title = show_title
        self.hide_footer = hide_footer
        self.content_or_url = content_or_url
        self.external_url = external_url
        self.element = element
        self.own_content = own_content

    @property
    def title(self):
        return self.ptitle or _(u"Existing Content")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/new_existing_content.pt')

    @memoize
    def owncontent(self):

        owncontent_path = self.data.own_content
        if not owncontent_path:
            return None

        if owncontent_path.startswith('/'):
            owncontent_path = owncontent_path[1:]
        if not owncontent_path:
            return None
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.unrestrictedTraverse(owncontent_path, default=None)

    def get_catalog_content(self):
        """ Fem una consulta al catalog, en comptes de fer un PyQuery """
        content = self.owncontent()
        if content.Type() == 'FormFolder':
            content = content.getObject()()
        else:
            content = self.owncontent()
        return content

    def checkContentIsPublic(self):
        if self.data.content_or_url == 'INTERN':
            content = self.get_catalog_content()
            if not content.expiration_date:
                return True

            now = DateTime.DateTime()
            return now >= content.effective_date and now <= content.expiration_date
        else:
            return True

    def getHTML(self):
        """ Agafa contingut de 'Element' de la 'URL', paràmetres definits per l'usuari
            Avisa si hi ha problemes en la URL o si no troba Element.
        """
        content = ''
        try:
            # CONTINGUT INTERN #

            if self.data.content_or_url == 'INTERN':
                # link intern, search through the catalog
                raw_html = self.get_catalog_content()()
                charset = re.findall('charset=(.*)"', raw_html)
                if len(charset) > 0:
                    clean_html = re.sub(r'[\n\r]?', r'', raw_html.encode(charset[0]))
                    doc = pq(clean_html)
                    if doc(self.data.element):
                        content = pq('<div/>').append(doc(self.data.element).outerHtml()).html(method='html')
                    else:
                        content = _(u"ERROR. This element does not exist:") + " " + self.data.element
                else:
                    content = _(u"ERROR. Charset undefined")

            # CONTENIDO EXTERNO #

            elif self.data.content_or_url == 'EXTERN':
                # link extern, pyreq
                link_extern = self.data.external_url
                raw_html = requests.get(link_extern, timeout=5)
                charset = re.findall('charset=(.*)"', raw_html.content)
                if len(charset) > 0:
                    clean_html = re.sub(r'[\n\r]?', r'', raw_html.content.decode(charset[0]))
                    doc = pq(clean_html)
                    if doc(self.data.element):
                        content = pq('<div/>').append(doc(self.data.element).outerHtml()).html(method='html')
                    else:
                        content = _(u"ERROR. This element does not exist:") + " " + self.data.element
                else:
                    content = _(u"ERROR. Charset undefined")

            # PORTLET MALAMENT CONFIGURAT #

            else:
                content = _(u"ERROR. Review the portlet configuration.")

        except ReadTimeout:
            content = _(u"ERROR. There was a timeout.")
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


class AddForm(base.AddForm):
    form_fields = form.Fields(INewContentPortlet)
    label = _(u"Afegeix portlet de contingut existent")
    description = _(u"Aquest portlet mostra contingut ja existent en URL específica")
    form_fields['own_content'].custom_widget = UberSelectionWidget

    def create(self, data):
        # s'invoca despres de __init__ en clicar Desa
        assignment = Assignment(**data)
        return assignment


class EditForm(base.EditForm):
    form_fields = form.Fields(INewContentPortlet)
    label = _(u"Edita portlet de contingut existent")
    description = _(u"Aquest portlet mostra contingut ja existent en URL específica.")
    form_fields['own_content'].custom_widget = UberSelectionWidget
