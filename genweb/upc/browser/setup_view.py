# -*- coding: utf-8 -*-
from five import grok
from plone import api
from cgi import parse_qs
from zope.event import notify
from zope.interface import alsoProvides
from zope.component import getMultiAdapter
from zope.component import queryUtility

from zope.lifecycleevent import ObjectModifiedEvent

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.dexterity.utils import createContentInContainer
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.app.controlpanel.mail import IMailSchema
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.multilingual.interfaces import ITranslationManager

from genweb.core.interfaces import IHomePage
from genweb.core.interfaces import INewsFolder
from genweb.core.interfaces import IEventFolder
from genweb.core.interfaces import IProtectedContent
from genweb.core.browser.plantilles import get_plantilles

import transaction

grok.templatedir('views_templates')

NEWS_QUERY = [{'i': u'portal_type', 'o': u'plone.app.querystring.operation.selection.is', 'v': [u'News Item']}, {'i': u'review_state', 'o': u'plone.app.querystring.operation.selection.is', 'v': [u'published']}]
QUERY_SORT_ON = u'effective'
EVENT_QUERY = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is', 'v': ['Event']}, {'i': 'start', 'o': 'plone.app.querystring.operation.date.afterToday', 'v': ''}, {'i': 'review_state', 'o': 'plone.app.querystring.operation.selection.is', 'v': ['published']}]


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
        setupTool = SetupMultilingualSite()
        setupTool.setupSite(self.context, False)

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

        # Hide 'Members' folder
        if getattr(portal, 'Members', False):
            api.content.delete(obj=portal['Members'])

        # Rename the original 'news' and 'events' folders for using it at the setup
        if getattr(portal, 'news', False):
            api.content.delete(obj=portal['news'])
            # api.content.rename(obj=portal['news'], new_id='news_setup')
        if getattr(portal, 'events', False):
            api.content.delete(obj=portal['events'])
            # api.content.rename(obj=portal['events'], new_id='events_setup')

        pc = api.portal.get_tool('portal_catalog')
        pc.clearFindAndRebuild()

        # Let's create folders and collections, linked by language, the first language is the canonical one

        # Setup portal news folder
        news = self.create_content(portal_en, 'Folder', 'news', title='News', description=u'Site news')
        noticias = self.create_content(portal_es, 'Folder', 'noticias', title='Notícias', description=u'Notícias del sitio')
        noticies = self.create_content(portal_ca, 'Folder', 'noticies', title='Notícies', description=u'Notícies del lloc')
        self.link_translations([(news, 'en'), (noticias, 'es'), (noticies, 'ca')])

        # Set layout for news folders
        news.setLayout('newscollection_view')
        noticias.setLayout('newscollection_view')
        noticies.setLayout('newscollection_view')

        news.exclude_from_nav = True
        noticias.exclude_from_nav = True
        noticies.exclude_from_nav = True

        # Create the aggregator
        col_news = self.create_content(news, 'Collection', 'aggregator', title='aggregator', description=u'Site news')
        col_news.title = 'News'
        col_news.query = NEWS_QUERY
        col_news.sort_on = QUERY_SORT_ON

        col_news.reindexObject()

        col_noticias = self.create_content(noticias, 'Collection', 'aggregator', title='aggregator', description=u'Notícias del sitio')
        col_noticias.title = 'Noticias'
        col_noticias.query = NEWS_QUERY
        col_noticias.sort_on = QUERY_SORT_ON

        col_noticias.reindexObject()

        col_noticies = self.create_content(noticies, 'Collection', 'aggregator', title='aggregator', description=u'Notícies del lloc')
        col_noticies.title = 'Notícies'
        col_noticies.query = NEWS_QUERY
        col_noticies.sort_on = QUERY_SORT_ON

        col_noticies.reindexObject()

        self.link_translations([(col_news, 'en'), (col_noticias, 'es'), (col_noticies, 'ca')])

        self.constrain_content_types(news, ('News Item', 'Folder', 'Image'))
        self.constrain_content_types(noticias, ('News Item', 'Folder', 'Image'))
        self.constrain_content_types(noticies, ('News Item', 'Folder', 'Image'))

        # Setup portal events folder
        events = self.create_content(portal_en, 'Folder', 'events', title='Events', description=u'Site events')
        eventos = self.create_content(portal_es, 'Folder', 'eventos', title='Eventos', description=u'Eventos del sitio')
        esdeveniments = self.create_content(portal_ca, 'Folder', 'esdeveniments', title='Esdeveniments', description=u'Esdeveniments del lloc')
        self.link_translations([(events, 'en'), (eventos, 'es'), (esdeveniments, 'ca')])

        events.exclude_from_nav = True
        eventos.exclude_from_nav = True
        esdeveniments.exclude_from_nav = True

        # Create the aggregator
        # original_col_events = original_events['aggregator']
        col_events = self.create_content(events, 'Collection', 'aggregator', title='aggregator', description=u'Site events')
        col_events.title = 'Events'
        col_events.query = EVENT_QUERY
        col_events.sort_on = QUERY_SORT_ON

        col_events.reindexObject()

        col_eventos = self.create_content(eventos, 'Collection', 'aggregator', title='aggregator', description=u'Eventos del sitio')
        col_eventos.title = 'Eventos'
        col_eventos.query = EVENT_QUERY
        col_eventos.sort_on = QUERY_SORT_ON

        col_eventos.reindexObject()

        col_esdeveniments = self.create_content(esdeveniments, 'Collection', 'aggregator', title='aggregator', description=u'Esdeveniments del lloc')
        col_esdeveniments.title = 'Esdeveniments'
        col_esdeveniments.query = EVENT_QUERY
        col_esdeveniments.sort_on = QUERY_SORT_ON

        col_esdeveniments.reindexObject()

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

        logosfooter_en = self.create_content(portal_en, 'Logos_Container', 'logosfooter-en', title='logosfooter-en', description=u'English footer logos')
        logosfooter_en.title = 'Footer Logos'
        logosfooter_es = self.create_content(portal_es, 'Logos_Container', 'logosfooter-es', title='logosfooter-es', description=u'Logos en español del pie de página')
        logosfooter_es.title = 'Logos pie'
        logosfooter_ca = self.create_content(portal_ca, 'Logos_Container', 'logosfooter-ca', title='logosfooter-ca', description=u'Logos en català del peu de pàgina')
        logosfooter_ca.title = 'Logos peu'
        self.link_translations([(logosfooter_ca, 'ca'), (logosfooter_es, 'es'), (logosfooter_en, 'en')])

        logosfooter_en.exclude_from_nav = True
        logosfooter_es.exclude_from_nav = True
        logosfooter_ca.exclude_from_nav = True

        logosfooter_en.reindexObject()
        logosfooter_es.reindexObject()
        logosfooter_ca.reindexObject()

        # welcome pages
        welcome_string = u"""<div>
<div class="destacatBandejat">
<p class="xxl" style="text-align: center; ">Contingut de la pàgina "Benvingut"</p>
</div>
<br />
</div>
<div>Actualitzeu aquí el contingut que voleu visualitzar a la pàgina principal del vostre web.</div>
<div>
<ul class="list list-highlighted">
<li><a class="external-link" href="http://genweb.upc.edu/documentacio" target="_blank" title="">Documentació Genweb v4</a></li>
</ul>
<br />
</div>
<div>
<div class="destacatBandejat">
<p class="xxl" style="text-align: center; ">Contenido de la página "Bienvenido"</p>
</div>

<div>Actualizad aquí el contenido que queréis visualizar en la página principal de vuestra web.</div>
<br /><br /><br />
<div class="destacatBandejat">
<p class="xxl" style="text-align: center; ">"Welcome" page content</p>
</div>
<div>Update here the content you want in your website home page.</div>
</div>
"""

        if not getattr(portal_en, 'welcome', False):
            welcome = self.create_content(portal_en, 'Document', 'welcome', title='Welcome')
            welcome.text = IRichText['text'].fromUnicode(welcome_string)
        if not getattr(portal_es, 'bienvenido', False):
            bienvenido = self.create_content(portal_es, 'Document', 'bienvenido', title='Bienvenido')
            bienvenido.text = IRichText['text'].fromUnicode(welcome_string)
        if not getattr(portal_ca, 'benvingut', False):
            benvingut = self.create_content(portal_ca, 'Document', 'benvingut', title='Benvingut')
            benvingut.text = IRichText['text'].fromUnicode(welcome_string)

        welcome = portal_en['welcome']
        bienvenido = portal_es['bienvenido']
        benvingut = portal_ca['benvingut']

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

        # Create default custom contact form info objects
        if not getattr(portal_en, 'customizedcontact', False):
            customizedcontact = self.create_content(portal_en, 'Document', 'customizedcontact', title='customizedcontact', publish=False)
            customizedcontact.title = u'Custom contact'
        if not getattr(portal_es, 'contactopersonalizado', False):
            contactopersonalizado = self.create_content(portal_es, 'Document', 'contactopersonalizado', title='contactopersonalizado', publish=False)
            contactopersonalizado.title = u'Contacto personalizado'
        if not getattr(portal_ca, 'contactepersonalitzat', False):
            contactepersonalitzat = self.create_content(portal_ca, 'Document', 'contactepersonalitzat', title='contactepersonalitzat', publish=False)
            contactepersonalitzat.title = u'Contacte personalitzat'

        customizedcontact = portal_en['customizedcontact']
        contactopersonalizado = portal_es['contactopersonalizado']
        contactepersonalitzat = portal_ca['contactepersonalitzat']

        customizedcontact.exclude_from_nav = True
        contactopersonalizado.exclude_from_nav = True
        contactepersonalitzat.exclude_from_nav = True

        # Templates TinyMCE
        templates = self.create_content(portal, 'Folder', 'templates', title='Templates', description='Plantilles per defecte administrades per l\'SC.')
        plantilles = self.create_content(portal, 'Folder', 'plantilles', title='Plantilles', description='En aquesta carpeta podeu posar les plantilles per ser usades a l\'editor.')

        templates.exclude_from_nav = True
        plantilles.exclude_from_nav = True

        templates.reindexObject()

        try:
            api.content.transition(obj=templates, transition='restrict')
        except:
            pass

        for plt in get_plantilles():
            plantilla = self.create_content(templates, 'Document', normalizeString(plt['titol']), title=plt['titol'], description=plt['resum'])
            plantilla.text = IRichText['text'].fromUnicode(plt['cos'])
            plantilla.reindexObject()

        api.content.transition(obj=plantilles, transition='retracttointranet')
        api.content.transition(obj=plantilles, transition='publish')
        plantilles.reindexObject()

        # Create the shared folders for files and images
        compartits = self.create_content(portal_ca, 'LIF', 'shared', title='shared', description='En aquesta carpeta podeu posar els fitxers i imatges que siguin compartits per tots o alguns idiomes.')
        compartits.title = 'Fitxers compartits'
        shared = self.create_content(portal_en, 'LIF', 'shared', title='shared', description='En aquesta carpeta podeu posar els fitxers i imatges que siguin compartits per tots o alguns idiomes.')
        shared.title = 'Shared files'
        compartidos = self.create_content(portal_es, 'LIF', 'shared', title='shared', description='En aquesta carpeta podeu posar els fitxers i imatges que siguin compartits per tots o alguns idiomes.')
        compartidos.title = 'Ficheros compartidos'
        self.constrain_content_types(compartits, ('File', 'Folder', 'Image'))
        self.constrain_content_types(shared, ('File', 'Folder', 'Image'))
        self.constrain_content_types(compartidos, ('File', 'Folder', 'Image'))

        compartits.exclude_from_nav = True
        shared.exclude_from_nav = True
        compartidos.exclude_from_nav = True

        compartits.reindexObject()
        shared.reindexObject()
        compartidos.reindexObject()

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
        alsoProvides(logosfooter_ca, IProtectedContent)
        alsoProvides(logosfooter_es, IProtectedContent)
        alsoProvides(logosfooter_en, IProtectedContent)
        alsoProvides(customizedcontact, IProtectedContent)
        alsoProvides(contactopersonalizado, IProtectedContent)
        alsoProvides(contactepersonalitzat, IProtectedContent)
        alsoProvides(shared, IProtectedContent)
        alsoProvides(compartidos, IProtectedContent)
        alsoProvides(compartits, IProtectedContent)

        # Mark also the special folders
        alsoProvides(noticies, INewsFolder)
        alsoProvides(noticias, INewsFolder)
        alsoProvides(news, INewsFolder)
        alsoProvides(esdeveniments, IEventFolder)
        alsoProvides(eventos, IEventFolder)
        alsoProvides(events, IEventFolder)

        # transaction.commit()
        pc.clearFindAndRebuild()

        # Put navigation portlets in place
        target_manager_en = queryUtility(IPortletManager, name='plone.leftcolumn', context=portal_en)
        target_manager_en_assignments = getMultiAdapter((portal_en, target_manager_en), IPortletAssignmentMapping)
        target_manager_es = queryUtility(IPortletManager, name='plone.leftcolumn', context=portal_es)
        target_manager_es_assignments = getMultiAdapter((portal_es, target_manager_es), IPortletAssignmentMapping)
        target_manager_ca = queryUtility(IPortletManager, name='plone.leftcolumn', context=portal_ca)
        target_manager_ca_assignments = getMultiAdapter((portal_ca, target_manager_ca), IPortletAssignmentMapping)
        from plone.app.portlets.portlets.navigation import Assignment as navigationAssignment
        if 'navigation' not in target_manager_en_assignments:
            target_manager_en_assignments['navigation'] = navigationAssignment(topLevel=1)
        if 'navigation' not in target_manager_es_assignments:
            target_manager_es_assignments['navigation'] = navigationAssignment(topLevel=1)
        if 'navigation' not in target_manager_ca_assignments:
            target_manager_ca_assignments['navigation'] = navigationAssignment(topLevel=1)

        # Delete default Navigation portlet on root
        target_manager_root = queryUtility(IPortletManager, name='plone.leftcolumn', context=portal)
        target_manager_root_assignments = getMultiAdapter((portal, target_manager_root), IPortletAssignmentMapping)
        if 'navigation' in target_manager_root_assignments:
            del target_manager_root_assignments['navigation']

        return True

    def create_content(self, container, portal_type, id, publish=True, **kwargs):
        if not getattr(container, id, False):
            obj = createContentInContainer(container, portal_type, checkConstraints=False, **kwargs)
            if publish:
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
            api.content.transition(obj=context, transition={'genweb_simple': 'publish', 'genweb_review': 'publicaalaintranet'}[object_workflow])
        #     try:
        #         pw.doActionFor(context, {'genweb_simple': 'publish', 'genweb_review': 'publicaalaintranet'}[object_workflow])
        #     except:
        #         pass
