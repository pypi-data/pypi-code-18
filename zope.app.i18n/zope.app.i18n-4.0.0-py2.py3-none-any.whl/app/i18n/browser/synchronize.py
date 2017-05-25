##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Synchronize with Foreign Translation Domains

"""
__docformat__ = 'restructuredtext'

try:
    import httplib
    from xmlrpclib import Transport
    from xmlrpclib import Server
    from xmlrpclib import ProtocolError
except ImportError:
    from xmlrpc.client import Transport
    from xmlrpc.client import ProtocolError
    from xmlrpc.client import ServerProxy as Server

try:
    from urllib import unquote
    from urllib import quote
    from urlparse import urlparse
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import unquote
    from urllib.parse import quote
    from urllib.parse import urlparse
    from urllib.parse import urlunparse

from base64 import encodestring

import zope.i18nmessageid

from zope.security.proxy import removeSecurityProxy

from zope.app.i18n.browser import BaseView

_ = zope.i18nmessageid.MessageFactory("zope")

DEFAULT = 'http://localhost:8080/++etc++site/default/zope'

class Synchronize(BaseView):

    messageStatus = [_('Up to Date'), _('New Remote'), _('Out of Date'),
                     _('Newer Local'), _('Does not exist')]

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.sync_url = self.request.cookies.get(
            'sync_url', DEFAULT)
        self.sync_url = unquote(self.sync_url)
        self.sync_username = self.request.cookies.get('sync_username', 'admin')
        self.sync_password = self.request.cookies.get('sync_password', 'admin')
        self.sync_languages = filter(None, self.request.cookies.get(
            'sync_languages', '').split(','))
        self._connection = None

    def _make_sync_url(self):
        # make sure the URL contains the http:// prefix
        url = self.sync_url
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        # Add username and password to the url.
        parts = urlparse(url)
        if '@' not in parts.netloc:
            parts = list(parts)
            parts[1] = self.sync_username + ':' + self.sync_password + '@' + parts[1]
            url = urlunparse(parts)

        return url

    def _connect(self):
        '''Connect to the remote server via XML-RPC HTTP; return status'''

        # Now try to connect
        self._connection = Server(self._make_sync_url())

        # check whether the connection was made and the Master Babel Tower
        # exists
        try:
            self._connection.getAllLanguages()
            return 1 # pragma: no cover
        except Exception:
            self._connection = None
            return 0

    def _disconnect(self):
        '''Disconnect from the sever; return ``None``'''
        self._connection = None

    def _isConnected(self):
        '''Check whether we are currently connected to the server; return
        boolean'''

        return bool(self._connection is not None and self._connection.getAllLanguages())

    def canConnect(self):
        '''Checks whether we can connect using this server and user data;
        return boolean'''
        if self._isConnected():
            return True

        return self._connect()

    def getAllLanguages(self):
        connected = self._isConnected()
        if not connected: connected = self._connect()

        if connected:
            return self._connection.getAllLanguages()
        return []


    def queryMessages(self):
        connected = self._isConnected()
        if not connected: connected = self._connect()

        fmsgs = []
        if connected:
            fmsgs = self._connection.getMessagesFor(self.sync_languages)

        return self.context.getMessagesMapping(self.sync_languages,
                                               fmsgs)

    def queryMessageItems(self):
        items = self.queryMessages().items()
        items = removeSecurityProxy(items)
        return sorted(items, key=lambda x: x[0][0] + x[0][1])

    def getStatus(self, fmsg, lmsg, verbose=1):
        state = 0
        if fmsg is None:
            state = 4
        elif lmsg is None:
            state = 1
        elif fmsg['mod_time'] > lmsg['mod_time']:
            state = 2
        elif fmsg['mod_time'] < lmsg['mod_time']:
            state = 3
        elif fmsg['mod_time'] == lmsg['mod_time']:
            state = 0

        return self.messageStatus[state] if verbose else state

    def saveSettings(self):
        self.sync_languages = self.request.form.get('sync_languages', [])
        self.request.response.setCookie('sync_languages',
                                        ','.join(self.sync_languages))
        self.request.response.setCookie('sync_url',
                                        quote(self.request['sync_url']).strip())
        self.request.response.setCookie('sync_username',
                                        self.request['sync_username'])
        self.request.response.setCookie('sync_password',
                                        self.request['sync_password'])

        return self.request.response.redirect(self.request.URL[-1] +
                                              '/@@synchronizeForm.html')


    def synchronize(self):
        mapping = self.queryMessages()
        self.context.synchronize(mapping)
        return self.request.response.redirect(self.request.URL[-1]+
                                                   '/@@synchronizeForm.html')


    def synchronizeMessages(self):
        idents = []
        for id in self.request.form['message_ids']:
            msgid = self.request.form['update-msgid-'+id]
            language = self.request.form['update-language-'+id]
            idents.append((msgid, language))

        mapping = self.queryMessages()
        new_mapping = {}
        for item in mapping.items():
            if item[0] in idents:
                new_mapping[item[0]] = item[1]

        self.context.synchronize(new_mapping)
        return self.request.response.redirect(self.request.URL[-1]+
                                                   '/@@synchronizeForm.html')
