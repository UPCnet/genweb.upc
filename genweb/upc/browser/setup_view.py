# -*- coding: utf-8 -*-
from five import grok
from plone import api
from cgi import parse_qs
from Acquisition import aq_parent
from zope.interface import alsoProvides
from zope.component import getMultiAdapter

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import _createObjectByType

from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.dexterity.utils import createContentInContainer

from plone.app.controlpanel.mail import IMailSchema
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.multilingual.interfaces import ITranslationManager

from genweb.core.interfaces import IHomePage
from genweb.core.interfaces import IProtectedContent
from genweb.core.browser.plantilles import get_plantilles

grok.templatedir('views_templates')


class setup(grok.View):
    grok.name('setup-view')
    grok.template('setup_view')
    grok.context(IPloneSiteRoot)
    grok.require('cmf.ManagePortal')

    # index = ViewPageTemplateFile('setup_view.pt')

    def update(self):
        base_url = "%s/@@setup-view" % str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        qs = self.request.get('QUERY_STRING', None)
        if qs is not None:
            query = parse_qs(qs)
            if 'create' in query:
                for name in query['create']:
                    if name == 'all':
                        self.setup_multilingual()
                        self.createContent()
                        self.request.response.redirect(base_url)

    def contentStatus(self):
        objects = [('Notícies', ['noticies', 'noticias', 'news']),
                   ('Esdeveniments', ['esdeveniments', 'eventos', 'events']),
                   ('Banners', ['banners-ca', 'banners-es', 'banners-en']),
                   ('LogosFooter', ['logosfooter-ca', 'logosfooter-es', 'logosfooter-en']),
                   ('Homepage', ['benvingut', 'bienvenido', 'welcome']),
                   ('Templates', ['templates', ]),
                   ('Plantilles', ['plantilles', ]),
                   ]
        result = []
        portal = api.portal.get()
        for o in objects:
            tr = [o[0]]
            for td in o[1]:
                tr.append(getattr(portal, td, False) and 'Creat' or 'No existeix')
            result.append(tr)
        return result

    def setup_multilingual(self):
        portal = api.portal.get()

        setupTool = SetupMultilingualSite()
        setupTool.setupSite(self.context, False)

        # Move 'news' and 'events' folders to its place on EN tree
        if getattr(portal, 'news', False):
            api.content.move(portal['news'], portal['en'])
        if getattr(portal, 'events', False):
            api.content.move(portal['events'], portal['en'])

    def createContent(self):
        """ Method that creates all the default content """
        portal = api.portal.get()
        portal_ca = portal['ca']
        portal_en = portal['en']
        portal_es = portal['es']

        # Let's configure mail
        mail = IMailSchema(portal)
        mail.smtp_host = u'localhost'
        mail.email_from_name = "Administrador del Genweb"
        mail.email_from_address = "noreply@upc.edu"

#         if getattr(portal, 'front-page', False):
#             portal.manage_delObjects('front-page')
#         if getattr(portal, 'news', False):
#             if not self.getObjectStatus(portal.news):
#                 portal.manage_delObjects('news')
#         if getattr(portal, 'events', False):
#             if not self.getObjectStatus(portal.events):
#                 portal.manage_delObjects('events')
#         if getattr(portal, 'Members', False):
#             portal['Members'].setExcludeFromNav(True)
#             portal['Members'].reindexObject()
#             portal['Members'].setLanguage('en')

        # Let's create folders and collections, linked by language, the first language is the canonical one

        # Setup portal news folder
        news = portal_en['news']
        noticias = self.create_content(portal_es, 'Folder', 'noticias', title='Notícias', description=u'Notícias del sitio')
        noticies = self.create_content(portal_ca, 'Folder', 'noticies', title='Notícies', description=u'Notícies del lloc')
        self.link_translations([(news, 'en'), (noticias, 'es'), (noticies, 'ca')])

        col_news = news['aggregator']
        col_noticias = self.create_content(noticias, 'Collection', 'aggregator', title='aggregator', description=u'Notícias del sitio')
        col_noticias.title = 'Notícias'
        self.clone_collection_settings(col_news, col_noticias)

        col_noticies = self.create_content(noticies, 'Collection', 'aggregator', title='aggregator', description=u'Notícies del lloc')
        col_noticies.title = 'Notícies'
        self.clone_collection_settings(col_news, col_noticies)
        self.link_translations([(col_news, 'en'), (col_noticias, 'es'), (col_noticies, 'ca')])

        # Setup portal events folder
        events = portal_en['events']
        eventos = self.create_content(portal_es, 'Folder', 'eventos', title='Eventos', description=u'Eventos del sitio')
        esdeveniments = self.create_content(portal_ca, 'Folder', 'esdeveniments', title='Esdeveniments', description=u'Esdeveniments del lloc')
        self.link_translations([(events, 'en'), (eventos, 'es'), (esdeveniments, 'ca')])

        col_events = events['aggregator']
        col_eventos = self.create_content(eventos, 'Collection', 'aggregator', title='aggregator', description=u'Eventos del sitio')
        col_eventos.title = 'Eventos'
        self.clone_collection_settings(col_events, col_eventos)

        col_esdeveniments = self.create_content(esdeveniments, 'Collection', 'aggregator', title='aggregator', description=u'Esdeveniments del lloc')
        col_esdeveniments.title = 'Esdeveniments'
        self.clone_collection_settings(col_news, col_esdeveniments)
        self.link_translations([(col_events, 'en'), (col_eventos, 'es'), (col_esdeveniments, 'ca')])

#         self.addCollection(events.aggregator, 'previous', 'Past Events', 'Events which have already happened. ', 'Event', dateRange=u'-', operation=u'less', setDefault=False, path='grandfather', date_filter=True)
#         self.addCollection(eventos.aggregator, 'anteriores', 'Eventos pasados', 'Eventos del sitio que ya han sucedido', 'Event', dateRange=u'-', operation=u'less', setDefault=False, path='grandfather', date_filter=True)
#         self.addCollection(esdeveniments.aggregator, 'anteriors', 'Esdeveniments passats', 'Esdeveniments del lloc que ja han passat', 'Event', dateRange=u'-', operation=u'less', setDefault=False, path='grandfather', date_filter=True)
#         self.setLanguageAndLink([(esdeveniments.aggregator.anteriors, 'ca'), (eventos.aggregator.anteriores, 'es'), (events.aggregator.previous, 'en')])

        banners_en = self.create_content(portal_en, 'BannerContainer', 'banners-en', title='banners-en', description=u'English Banners')
        banners_en.title = 'Banners'
        banners_es = self.create_content(portal_es, 'BannerContainer', 'banners-es', title='banners-es', description=u'Banners en Español')
        banners_es.title = 'Banners'
        banners_ca = self.create_content(portal_ca, 'BannerContainer', 'banners-ca', title='banners-ca', description=u'Banners en Català')
        banners_ca.title = 'Banners'
        self.link_translations([(banners_ca, 'ca'), (banners_es, 'es'), (banners_en, 'en')])

#         logosfooter_en = self.crearObjecte(portal, 'logosfooter-en', 'Logos_Container', 'Footer Logos', 'English footer logos')
#         logosfooter_es = self.crearObjecte(portal, 'logosfooter-es', 'Logos_Container', 'Logos pie', 'Logos en español del pie de página')
#         logosfooter_ca = self.crearObjecte(portal, 'logosfooter-ca', 'Logos_Container', 'Logos peu', 'Logos en català del peu de pàgina')
#         self.setLanguageAndLink([(logosfooter_ca, 'ca'), (logosfooter_es, 'es'), (logosfooter_en, 'en')])

        # welcome pages
        welcome_string = u"""<h1 class="documentFirstHeading">Us donem la benvinguda a Genweb UPC v4, el genweb "mobilitzat"!</p>
<p>Aquesta versió incorpora millores en el disseny i la flexibilitat, s’ha adaptat als dispositius mòbils i s’hi han inclòs moltes de les vostres demandes. Les voleu conèixer en detall?<br/><br/>I a partir d'ara, ja podreu introduir els continguts.</p>

<h2>Abans d'utilitzar Genweb...</h2>
<p>Aneu a Comunitat Genweb, conegueu les darreres novetats amb Genweb Tour, consulteu la Guia ràpida i els Exemples pràctics, i informeu-vos dels Recursos d’edició i de tota la documentació i ajuts que teniu a la vostra disposició.</p>

<h2>I quan el tingueu llest...</h2>
<p>Podreu disposar d’allotjament per al web, d’un domini upc.edu, d’estadístiques d’accés, de formació i de suport tècnic.</p>
"""

        welcome = self.create_content(portal_en, 'Document', 'welcome', title='Welcome')
        bienvenido = self.create_content(portal_es, 'Document', 'bienvenido', title='Bienvenido')
        benvingut = self.create_content(portal_ca, 'Document', 'benvingut', title='Benvingut')

        welcome.text = IRichText['text'].fromUnicode(welcome_string)
        bienvenido.text = IRichText['text'].fromUnicode(welcome_string)
        benvingut.text = IRichText['text'].fromUnicode(welcome_string)

        self.link_translations([(benvingut, 'ca'), (bienvenido, 'es'), (welcome, 'en')])

        # Mark all homes with IHomePage marker interface
        alsoProvides(benvingut, IHomePage)
        alsoProvides(bienvenido, IHomePage)
        alsoProvides(welcome, IHomePage)

        # Reindex them to update object_provides index
        benvingut.reindexObject()
        bienvenido.reindexObject()
        welcome.reindexObject()

        # Set the default pages to the homepage view
        portal_en.setLayout('homepage')
        portal_es.setLayout('homepage')
        portal_ca.setLayout('homepage')

#         # Templates TinyMCE
#         templates = self.crearObjecte(portal, 'templates', 'Folder', 'Templates', 'Plantilles per defecte administrades per l\'SCP.', constrains=(['Document'], ['']))
#         plantilles = self.crearObjecte(portal, 'plantilles', 'Folder', 'Plantilles', 'En aquesta carpeta podeu posar les plantilles per ser usades a l\'editor.', constrains=(['Document'], ['']))
#         pw = getToolByName(portal, "portal_workflow")
#         try:
#             pw.doActionFor(templates, "restrict")
#         except:
#             None

#         for plt in get_plantilles():
#             plantilla = self.crearObjecte(templates, normalizeString(plt['titol']), 'Document', plt['titol'], plt['resum'], '')
#             plantilla.setText(plt['cos'], mimetype="text/html")

        # Mark all protected content with the protected marker interface
        alsoProvides(benvingut, IProtectedContent)
        alsoProvides(bienvenido, IProtectedContent)
        alsoProvides(welcome, IProtectedContent)
        alsoProvides(noticies, IProtectedContent)
        alsoProvides(noticias, IProtectedContent)
        alsoProvides(news, IProtectedContent)
        alsoProvides(esdeveniments, IProtectedContent)
        alsoProvides(eventos, IProtectedContent)
        alsoProvides(events, IProtectedContent)
        alsoProvides(banners_ca, IProtectedContent)
        alsoProvides(banners_en, IProtectedContent)
        alsoProvides(banners_es, IProtectedContent)
        # alsoProvides(templates, IProtectedContent)
        # alsoProvides(plantilles, IProtectedContent)
        # alsoProvides(logosfooter_ca, IProtectedContent)
        # alsoProvides(logosfooter_es, IProtectedContent)
        # alsoProvides(logosfooter_en, IProtectedContent)

        return True

    def create_content(self, container, portal_type, id, **kwargs):
        if not getattr(container, id, False):
            obj = createContentInContainer(container, portal_type, checkConstraints=False, **kwargs)

        return getattr(container, id)

    def link_translations(self, items):
        """
            Links the translations with the declared items with the form:
            [(obj1, lang1), (obj2, lang2), ...] assuming that the first element
            is the 'canonical' (in PAM there is no such thing).
        """
        # Grab the first item object and get its canonical handler
        canonical = ITranslationManager(items[0][0])

        for obj, language in items:
            if not canonical.has_translation(language):
                canonical.register_translation(language, obj)

    def clone_collection_settings(self, origin, target):
        if getattr(origin, 'query', False):
            target.query = origin.query
        if getattr(origin, 'sort_on', False):
            target.sort_on = origin.sort_on
        if getattr(origin, 'sort_reversed', False):
            target.sort_reversed = origin.sort_reversed
        if getattr(origin, 'limit', False):
            target.limit = origin.limit
        if getattr(origin, 'item_count', False):
            target.item_count = origin.item_count
        if getattr(origin, 'customViewFields', False):
            target.customViewFields = origin.customViewFields

    def getObjectStatus(self, context):
        pw = getToolByName(context, "portal_workflow")
        object_workflow = pw.getWorkflowsFor(context)[0].id
        object_status = pw.getStatusOf(object_workflow, context)
        return object_status

    def doWorkflowAction(self, context):
        pw = getToolByName(context, "portal_workflow")
        object_workflow = pw.getWorkflowsFor(context)[0].id
        object_status = pw.getStatusOf(object_workflow, context)
        if object_status:
            try:
                pw.doActionFor(context, {'genweb_simple': 'publish', 'genweb_review': 'publicaalaintranet'}[object_workflow])
            except:
                pass

    def create_object(self, context, id, type_name, title, description, exclude=True, constrains=None):
        pt = getToolByName(context, 'portal_types')
        if not getattr(context, id, False) and type_name in pt.listTypeTitles().keys():
            #creem l'objecte i el publiquem
            _createObjectByType(type_name, context, id)
        #populem l'objecte
        created = context[id]
        self.doWorkflowAction(created)
        created.setTitle(title)
        created.setDescription(description)
        created._at_creation_flag = False
        created.setExcludeFromNav(exclude)
        if constrains:
            created.setConstrainTypesMode(1)
            if len(constrains) > 1:
                created.setLocallyAllowedTypes(tuple(constrains[0] + constrains[1]))
            else:
                created.setLocallyAllowedTypes(tuple(constrains[0]))
            created.setImmediatelyAddableTypes(tuple(constrains[0]))

        created.reindexObject()
        return created
