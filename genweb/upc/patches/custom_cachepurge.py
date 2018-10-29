from App.config import getConfiguration
from plone.cachepurging.interfaces import IPurger
from zope.interface import implementer
from zope.testing.cleanup import addCleanUp

import logging
import urlparse
import os

logger = logging.getLogger('plone.cachepurging')


def _purgeSync(self, conn, url, httpVerb):
    """Perform the purge request. Returns a triple
    ``(resp, xcache, xerror)`` where ``resp`` is the response object for
    the connection, ``xcache`` is the contents of the X-Cache header,
    and ``xerror`` is the contents of the first header found of the
    header list in ``self.errorHeaders``.
    """

    (scheme, host, path, params, query, fragment) = urlparse.urlparse(url)
    __traceback_info__ = (url, httpVerb, scheme, host,
                          path, params, query, fragment)

    if self.http_1_1:
        conn._http_vsn = 11
        conn._http_vsn_str = 'HTTP/1.1'
    else:
        conn._http_vsn = 10
        conn._http_vsn_str = 'HTTP/1.0'
        # When using HTTP 1.0, to make up for the lack of a 'Host' header
        # we use the full url as the purge path, to allow for virtual
        # hosting in squid
        path = url

    purge_path = urlparse.urlunparse(
        ('', '', path, params, query, fragment))
    logger.debug('making %s request to %s for %s.',
        httpVerb, host, purge_path)
    conn.putrequest(httpVerb, purge_path, skip_accept_encoding=True)
    conn.endheaders()
    resp = conn.getresponse()

    xcache = resp.getheader('x-cache', '')
    xerror = ''
    #import ipdb; ipdb.set_trace()
    ZOPE_HOME = os.environ['ZOPE_HOME']
    try:
        f = open( ZOPE_HOME +'/var/log/urls_to_purge','a')
        f.write(path + '\n')
        f.close()
    except IOError:
        logger.warning('Can not write to urls_to_purge file on %s/var/log', ZOPE_HOME)
    except KeyError:
        logger.warning('No env variable called ZOPE_HOME')
    for header in self.errorHeaders:
        xerror = resp.getheader(header, '')
        if xerror:
            # Break on first found.
            break
    resp.read()
    logger.debug("%s of %s: %s %s",
        httpVerb, url, resp.status, resp.reason)
    return resp, xcache, xerror
