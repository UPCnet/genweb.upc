# -*- coding: utf-8 -*-
from five import grok
from plone import api
from cgi import parse_qs
from zope.interface import alsoProvides
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.dexterity.utils import createContentInContainer

from plone.app.controlpanel.mail import IMailSchema
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.multilingual.interfaces import ITranslationManager
from plone.app.multilingual.browser.utils import multilingualMoveObject

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
        objects = [('Notícies', [('noticies', 'ca'), ('noticias', 'es'), ('news', 'en')]),
                   ('Esdeveniments', [('esdeveniments', 'ca'), ('eventos', 'es'), ('events', 'en')]),
                   ('Banners', [('banners-ca', 'ca'), ('banners-es', 'es'), ('banners-en', 'en')]),
                   ('LogosFooter', [('logosfooter-ca', 'ca'), ('logosfooter-es', 'es'), ('logosfooter-en', 'en')]),
                   ('Homepage', [('benvingut', 'ca'), ('bienvenido', 'es'), ('welcome', 'en')]),
                   ('Templates', [('templates', 'root')]),
                   ('Plantilles', [('plantilles', 'root')]),
                   ]
        result = []
        portal = api.portal.get()
        for o in objects:
            tr = [o[0]]
            for td, lang in o[1]:
                if lang == 'root':
                    tr.append(getattr(portal, td, False) and 'Creat' or 'No existeix')
                else:
                    if getattr(portal, lang, False):
                        tr.append(getattr(portal[lang], td, False) and 'Creat' or 'No existeix')
                    else:
                        tr.append('No existeix')
            result.append(tr)
        return result

    def setup_multilingual(self):
        portal = api.portal.get()

        setupTool = SetupMultilingualSite()
        setupTool.setupSite(self.context, False)

        # Move 'news' and 'events' folders to its place on EN tree
        if getattr(portal, 'news', False):
            multilingualMoveObject(portal['news'], 'en')
        if getattr(portal, 'events', False):
            multilingualMoveObject(portal['events'], 'en')

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

        # Get rid of the original page
        if getattr(portal_en, 'front-page', False):
            api.content.delete(obj=portal['front-page'])

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

        self.constrain_content_types(news, ('News Item', 'Folder', 'Image'))
        self.constrain_content_types(noticias, ('News Item', 'Folder', 'Image'))
        self.constrain_content_types(noticies, ('News Item', 'Folder', 'Image'))

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

        self.constrain_content_types(events, ('Event', 'Folder', 'Image'))
        self.constrain_content_types(eventos, ('Event', 'Folder', 'Image'))
        self.constrain_content_types(esdeveniments, ('Event', 'Folder', 'Image'))

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

        banners_en.exclude_from_nav = True
        banners_es.exclude_from_nav = True
        banners_ca.exclude_from_nav = True

        banners_en.reindexObject()
        banners_es.reindexObject()
        banners_ca.reindexObject()

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

        benvingut.exclude_from_nav = True
        bienvenido.exclude_from_nav = True
        welcome.exclude_from_nav = True

        # Reindex them to update object_provides index
        benvingut.reindexObject()
        bienvenido.reindexObject()
        welcome.reindexObject()

        # Set the default pages to the homepage view
        portal_en.setLayout('homepage')
        portal_es.setLayout('homepage')
        portal_ca.setLayout('homepage')

        # Templates TinyMCE
        templates = self.create_content(portal, 'Folder', 'templates', title='Templates', description='Plantilles per defecte administrades per l\'SC.')
        # templates = self.create_content(portal, 'Folder', 'templates', title='Templates', 'Plantilles per defecte administrades per l\'SC.', constrains=(['Document'], ['']))
        plantilles = self.create_content(portal, 'Folder', 'plantilles', title='Plantilles', description='En aquesta carpeta podeu posar les plantilles per ser usades a l\'editor.')
        # plantilles = self.create_content(portal, 'plantilles', 'Folder', 'Plantilles', 'En aquesta carpeta podeu posar les plantilles per ser usades a l\'editor.', constrains=(['Document'], ['']))
        try:
            api.content.transition(obj=templates, transition='restrict')
        except:
            pass

        for plt in get_plantilles():
            plantilla = self.create_content(templates, 'Document', normalizeString(plt['titol']), title=plt['titol'], description=plt['resum'])
            plantilla.text = IRichText['text'].fromUnicode(plt['cos'])

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
        alsoProvides(templates, IProtectedContent)
        alsoProvides(plantilles, IProtectedContent)
        # alsoProvides(logosfooter_ca, IProtectedContent)
        # alsoProvides(logosfooter_es, IProtectedContent)
        # alsoProvides(logosfooter_en, IProtectedContent)

        return True

    def create_content(self, container, portal_type, id, **kwargs):
        if not getattr(container, id, False):
            obj = createContentInContainer(container, portal_type, checkConstraints=False, **kwargs)
            self.publish_content(obj)
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

    def constrain_content_types(self, container, content_types):
        # Set on them the allowable content types
        behavior = ISelectableConstrainTypes(container)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(content_types)
        behavior.setImmediatelyAddableTypes(content_types)

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

    def publish_content(self, context):
        """ Make the content visible either in both possible genweb.simple and
            genweb.review workflows.
        """
        pw = getToolByName(context, "portal_workflow")
        object_workflow = pw.getWorkflowsFor(context)[0].id
        object_status = pw.getStatusOf(object_workflow, context)
        if object_status:
            try:
                pw.doActionFor(context, {'genweb_simple': 'publish', 'genweb_review': 'publicaalaintranet'}[object_workflow])
            except:
                pass
