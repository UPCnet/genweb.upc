# -- coding: utf-8 --

from Acquisition import aq_inner
from Products.Five.browser import BrowserView

from zope.interface import Interface
from zope.component import adapter
from ZPublisher.interfaces import IPubBeforeCommit


class CookiesManagement(BrowserView):
    """ Convenience view for faster debugging. Needs to be manager. """

    def the_title(self):
        return u'A list of talks:'

    def getTitle(self):
        # import ipdb; ipdb.set_trace()
        return u'Politica de cookies'
    
    def getCookies(self):
        req = self.request.cookies.get('l18N_LANGUAGE','ca')
        return req


