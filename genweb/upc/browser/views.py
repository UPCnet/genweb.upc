# -*- coding: utf-8 -*-
from five import grok
from plone import api
from Acquisition import aq_inner
from zope.interface import Interface
from scss import Scss

from DateTime.DateTime import DateTime
import pytz

from zope.annotation.interfaces import IAnnotations
from plone.app.contenttypes.interfaces import IEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize import ram

from genweb.upc.content.subhome import ISubhome
from genweb.upc.browser.interfaces import IGenwebUPC
from genweb.core.utils import genweb_config
from genweb.theme.browser.views import _render_cachekey, HomePageBase
from genweb.theme.browser.interfaces import IHomePageView

import pkg_resources
import scss

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.interfaces import IDexterityContent

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
from email.utils import formatdate

from cStringIO import StringIO


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

# iCal header and footer
ICS_HEADER = """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Plone.org//NONSGML plone.app.event//EN
X-WR-TIMEZONE:%(timezone)s
"""

ICS_FOOTER = """\
END:VCALENDAR
"""

# iCal event
ICS_EVENT_START = """\
BEGIN:VEVENT
SUMMARY:%(summary)s
DTSTART;TZID=%(timezone)s;VALUE=DATE-TIME:%(startdate)s
DTEND;TZID=%(timezone)s;VALUE=DATE-TIME:%(enddate)s
DTSTAMP;VALUE=DATE-TIME:%(dtstamp)s
UID:%(uid)s
"""

ICS_EVENT_END = """\
CONTACT:%(contact_name)s\, %(contact_email)s
CREATED;VALUE=DATE-TIME:%(created)s
LAST-MODIFIED;VALUE=DATE-TIME:%(modified)s
LOCATION:%(location)s
URL:%(url)s
END:VEVENT
"""

# iCal timezone
ICS_TIMEZONE_START = """\
BEGIN:VTIMEZONE
TZID:%(timezone)s
X-LIC-LOCATION:%(timezone)s
"""

ICS_TIMEZONE_END = """\
END:VTIMEZONE
"""

# iCal standard
ICS_STANDARD = """\
BEGIN:STANDARD
DTSTART;VALUE=DATE-TIME:20161030T020000
TZNAME:CET
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
END:STANDARD
"""

ATTENDEES_MESSAGE_TEMPLATE = """\
%(title)s

Iniciar: %(start)s
Final: %(end)s
Assistents: %(attendees)s
Descripció: %(description)s

S'adjunta un fitxer iCalendar amb més informació sobre l'esdeveniment.
"""


class gwSendEventView(grok.View):
    grok.context(IEvent)
    grok.name('send-event')
    grok.require('cmf.AddPortalContent')
    grok.layer(IGenwebUPC)

    def render(self):
        context = aq_inner(self.context)
        annotations = IAnnotations(context)
        event_title = context.Title().decode('utf-8')
        event_day = DateTime().day()
        event_month = DateTime().month()
        event_year = DateTime().year()
        event_hour = DateTime().Time()
        event_link = context.absolute_url()
        mailhost = getToolByName(context, 'MailHost')
        urltool = getToolByName(context, 'portal_url')
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')
        to_address = 'agenda.web@upc.edu'
        from_name = portal.getProperty('email_from_name')
        from_address = portal.getProperty('email_from_address')
        titulo_web = portal.getProperty('title').decode('utf-8')
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

        # afegim valors per defecte als colors i aixi sempre compila la css dinamica
        if not self.especific1:
            self.especific1 = '#007bc0'
        if not self.especific2:
            self.especific2 = '#557C95'

        if self.especific1 and self.especific2:
            return '@import "{}/genwebcustom.css";\n'.format(api.portal.get().absolute_url()) + \
                   self.compile_scss(especific1=self.especific1, especific2=self.especific2)
        else:
            default = '@import "{}/genwebcustom.css";'.format(api.portal.get().absolute_url())
            return default

    @ram.cache(_render_cachekey)
    def compile_scss(self, **kwargs):
        genwebupcegg = pkg_resources.get_distribution('genweb.upc')

        scssfile = open('{}/genweb/upc/scss/_dynamic.scss'.format(genwebupcegg.location))

        settings = dict(especific1=self.especific1,
                        especific2=self.especific2)

        variables_scss = """

        $genwebPrimary: {especific1};
        $genwebTitles: {especific2};

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


class ContactFeedback(grok.View):
    grok.name('contact_feedback')
    grok.context(INavigationRoot)
    grok.template("contact_feedback")
    grok.require('zope2.View')
    grok.layer(IGenwebUPC)

# from zope.component import queryUtility
# from plone.portlets.interfaces import IPortletManager
# from plone.portlets.interfaces import IPortletAssignmentMapping
# from zope.component import getMultiAdapter
# from plone.protect.interfaces import IDisableCSRFProtection
# from zope.interface import alsoProvides


# class SetNewsEventsListingPortlet(grok.View):
#     grok.name('set_newsevents_portlet')
#     grok.context(Interface)
#     grok.require('zope2.View')
#     grok.layer(IGenwebUPC)

#     def render(self):
#             alsoProvides(self.request, IDisableCSRFProtection)
#             target = queryUtility(IPortletManager, name='plone.leftcolumn', context=self.context)
#             assignments = getMultiAdapter((self.context, target), IPortletAssignmentMapping)
#             from genweb.theme.portlets.news_events_listing import Assignment as news_events_listing_Assignment
#             assignments['navigation'] = news_events_listing_Assignment([''], u'Events')

class SubhomeView(HomePageBase):
    """ This is the special view for the subhomepage containing support for the
        portlet managers provided by the package genweb.portlets.
        This is the PAM aware default LRF homepage view.
        It is also used in IFolderish (DX and AT) content for use in inner landing
        pages.
    """
    grok.name('subhome_view')
    grok.implements(IHomePageView)
    grok.context(ISubhome)
    grok.layer(IGenwebUPC)

    def render(self):
        template = ViewPageTemplateFile('views_templates/subhome_view.pt')
        return template(self)

# from Products.Five.browser import BrowserView
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
# from zope.component import getMultiAdapter, getUtility


class ArticleView(grok.View):
    grok.name('article')
    grok.require('zope2.View')
    grok.layer(IGenwebUPC)
    grok.context(Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self):
        template = ViewPageTemplateFile('views_templates/article.pt')
        return template(self)

    def getImageBrains(self):
        catalog = self.context.portal_catalog
        folder_path = '/'.join(self.context.getPhysicalPath()[:-1])
        return catalog.searchResults(path=dict(query=folder_path, depth=1),
                                     portal_type='Image',
                                     sort_on='getObjPositionInParent')


class SendEventToAttendees(grok.View):
    grok.context(IDexterityContent)
    grok.name('event_to_attendees')
    grok.require('cmf.ModifyPortalContent')
    grok.layer(IGenwebUPC)

    def render(self):
        portal = api.portal.get()
        context = aq_inner(self.context)
        subject = 'Invitació: %s\n' % self.context.Title()
        email_charset = portal.getProperty('email_charset')
        mailhost = getToolByName(context, 'MailHost')

        map = {
            'title': self.context.Title(),
            'start': self.applytz(self.context.start).strftime('%d/%m/%Y %H:%M:%S'),
            'end': self.applytz(self.context.end).strftime('%d/%m/%Y %H:%M:%S'),
            'attendees': ', '.join(self.context.attendees).encode('utf-8'),
            'description': self.context.Description()
            }

        body = ATTENDEES_MESSAGE_TEMPLATE % map
        msg = MIMEMultipart()
        msg['From'] = portal.getProperty('email_from_address')
        msg['To'] = ', '.join(self.context.attendees).encode('utf-8')
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject.decode('utf-8')

        msg.attach(MIMEText(body, 'plain'))
        msg.attach(self.get_ics())

        mailhost.send(msg)

    def get_ics(self):
        """iCalendar output
        """
        out = StringIO()

        out.write(ICS_HEADER % {'timezone': self.context.timezone})
        out.write(self.getICal())
        out.write(ICS_FOOTER)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(self.n2rn(out.getvalue()))
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s.ics"'
            % self.context.getId())

        return part

    def getICal(self):
        """get iCal data
        """
        out = StringIO()

        map = {
            'summary': self.vformat(self.context.Title()),
            'timezone': self.context.timezone,
            'startdate': self.rfc2445dtlocal(self.context.start),
            'enddate': self.rfc2445dtlocal(self.context.end),
            'dtstamp': self.rfc2445dt(DateTime()),
            'uid': self.context.sync_uid,
        }
        out.write(ICS_EVENT_START % map)

        for assistant in self.context.attendees:
            out.write('ATTENDEE;CN={0};ROLE=REQ-PARTICIPANT:{0}\n'.format(assistant.encode('utf-8')))

        for category in self.context.subject:
            out.write('CATEGORIES:%s\n' % category.encode('utf-8'))

        location = self.context.location.encode('utf-8') if self.context.location else None
        map = {
            'contact_name': self.context.contact_name,
            'contact_email': self.context.contact_email,
            'created': self.rfc2445dt(self.context.creation_date),
            'modified': self.rfc2445dt(self.context.modification_date),
            'location': location,
            'url': self.context.absolute_url(),
        }
        out.write(ICS_EVENT_END % map)

        map = {
            'timezone': self.context.timezone,
        }
        out.write(ICS_TIMEZONE_START % map)

        out.write(ICS_STANDARD)
        out.write(ICS_TIMEZONE_END)

        return out.getvalue()

    def vformat(self, s):
        # return string with escaped commas and semicolons
        # NOTE: RFC 2445 specifies "a COLON character in a 'TEXT' property value
        # SHALL NOT be escaped with a BACKSLASH character." So watch out for
        # non-TEXT values, should they be introduced later in this code!
        return s.strip().replace(', ', '\, ').replace(';', '\;')

    def n2rn(self, s):
        return s.replace('\n', '\r\n')

    def rfc2445dt(self, dt):
        # return UTC in RFC2445 format YYYYMMDDTHHMMSSZ
        return dt.HTML4().replace('-', '').replace(':', '')

    def rfc2445dtlocal(self, dt):
        # return UTC in RFC2445 format YYYYMMDDTHHMMSS
        return self.applytz(dt).strftime('%Y%m%dT%H%M%S')

    def applytz(self, dt):
        return dt.astimezone(pytz.timezone(self.context.timezone))
