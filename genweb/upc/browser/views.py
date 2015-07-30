# -*- coding: utf-8 -*-
from five import grok
from plone import api
from Acquisition import aq_inner
from zope.interface import Interface
from scss import Scss

from DateTime.DateTime import DateTime
from zope.annotation.interfaces import IAnnotations
from plone.app.contenttypes.interfaces import IEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from plone.memoize import ram

from genweb.upc.browser.interfaces import IGenwebUPC
from genweb.core.utils import genweb_config
from genweb.theme.browser.views import _render_cachekey

import pkg_resources
import scss

grok.templatedir("views_templates")

MESSAGE_TEMPLATE = u"""\
L'usuari %(user_name)s ha creat un nou esdeveniment en l'agenda del GenWeb \
"%(titolGW)s":

Títol: "%(titleEvent)s"
Data: %(dayEvent)s-%(monthEvent)s-%(yearEvent)s
Hora: %(hourEvent)s

i que podreu trobar al següent enllaç:

%(linkEvent)s

Per a la seva publicació a l'Agenda general de la UPC.
"""


class gwSendEventView(grok.View):
    grok.context(IEvent)
    grok.name('send-event')
    grok.require('cmf.AddPortalContent')
    grok.layer(IGenwebUPC)

    def render(self):
        context = aq_inner(self.context)
        annotations = IAnnotations(context)
        event_title = context.Title()
        event_start = context.startDate
        event_day = DateTime.day(event_start)
        event_month = DateTime.month(event_start)
        event_year = DateTime.year(event_start)
        event_hour = DateTime.Time(event_start)
        event_link = context.absolute_url()
        mailhost = getToolByName(context, 'MailHost')
        urltool = getToolByName(context, 'portal_url')
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')
        to_address = 'info@upc.edu'
        from_name = portal.getProperty('email_from_name')
        from_address = portal.getProperty('email_from_address')
        titulo_web = portal.getProperty('title')
        mtool = self.context.portal_membership
        userid = mtool.getAuthenticatedMember().id
        source = "%s <%s>" % (from_name, from_address)
        subject = "[Nou esdeveniment] %s" % (titulo_web)
        message = MESSAGE_TEMPLATE % dict(titolGW=titulo_web,
                                          titleEvent=event_title,
                                          dayEvent=event_day,
                                          monthEvent=event_month,
                                          yearEvent=event_year,
                                          hourEvent=event_hour,
                                          linkEvent=event_link,
                                          from_address=from_address,
                                          from_name=from_name,
                                          user_name=userid)

        mailhost.secureSend(message, to_address, source,
                            subject=subject, subtype='plain',
                            charset=email_charset, debug=False,
                            )

        if 'eventsent' not in annotations:
            annotations['eventsent'] = True

        confirm = _(u"Gràcies per la vostra col·laboració. Les dades de l\'activitat s\'han enviat correctament i seran publicades com més aviat millor.")
        IStatusMessage(self.request).addStatusMessage(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url())


class dynamicCSS(grok.View):
    grok.name('dynamic.css')
    grok.context(Interface)
    grok.layer(IGenwebUPC)

    def update(self):
        self.especific1 = genweb_config().especific1
        self.especific2 = genweb_config().especific2

    def render(self):
        self.request.response.setHeader('Content-Type', 'text/css')
        self.request.response.addHeader('Cache-Control', 'must-revalidate, max-age=0, no-cache, no-store')
        if self.especific1 and self.especific2:
            return self.compile_scss(especific1=self.especific1, especific2=self.especific2)
        else:
            default = '@import "{}/genwebcustom.css";'.format(api.portal.get().absolute_url())
            return default

    @ram.cache(_render_cachekey)
    def compile_scss(self, **kwargs):
        genwebupcegg = pkg_resources.get_distribution('genweb.upc')

        scssfile = open('{}/genweb/upc/scss/_dynamic.scss'.format(genwebupcegg.location))

        settings = dict(especific1=self.especific1,
                        especific2=self.especific2,
                        portal_url=api.portal.get().absolute_url())

        variables_scss = """

        $genwebPrimary: {especific1};
        $genwebTitles: {especific2};

        @import "{portal_url}/genwebcustom.css";

        """.format(**settings)

        scss.config.LOAD_PATHS = [
            '{}/genweb/upc/bootstrap/scss/compass_twitter_bootstrap'.format(genwebupcegg.location)
        ]

        css = Scss(scss_opts={
                   'compress': False,
                   'debug_info': False,
                   })

        dynamic_scss = ''.join([variables_scss, scssfile.read()])

        return css.compile(dynamic_scss)
