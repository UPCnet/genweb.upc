# -*- coding: utf-8 -*-
from five import grok
from plone import api
from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from zope.annotation.interfaces import IAnnotations
from plone.app.contenttypes.interfaces import IEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

from genweb.theme.browser.interfaces import IGenwebTheme

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
    grok.layer(IGenwebTheme)

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
