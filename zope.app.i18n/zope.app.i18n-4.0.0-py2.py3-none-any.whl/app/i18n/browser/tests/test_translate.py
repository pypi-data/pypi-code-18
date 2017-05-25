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
"""Test Translation Domain 'Translate' screen.

"""
import unittest
from io import BytesIO

from zope.component.testing import PlacelessSetup
from zope.component.interfaces import IFactory
from zope.component.factory import Factory
from zope.component import provideAdapter, provideUtility
from zope.component.testlayer import ZCMLFileLayer

import zope.app.i18n.tests

from zope.app.i18n.browser.translate import Translate as _Translate
from zope.app.i18n.translationdomain import TranslationDomain
from zope.app.i18n.messagecatalog import MessageCatalog
from zope.i18n.interfaces import IUserPreferredCharsets

from zope.publisher.http import IHTTPRequest
from zope.publisher.http import HTTPCharsets
from zope.publisher.browser import TestRequest as BrowserRequest

class Translate(_Translate):
    """Make Translate a valid Browser view. Usually done by ZCML."""

    def __init__(self, context, request):
        self.context = context
        self.request = request


class TranslateTest(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(TranslateTest, self).setUp()

        # Setup the registries
        provideAdapter(HTTPCharsets, (IHTTPRequest,), IUserPreferredCharsets)

        provideUtility(Factory(MessageCatalog), IFactory,
                       'zope.app.MessageCatalog')

        self._domain = domain = TranslationDomain()
        domain.domain = 'default'

        en_catalog = MessageCatalog('en', 'default')
        de_catalog = MessageCatalog('de', 'default')

        en_catalog.setMessage('short_greeting', 'Hello!')
        de_catalog.setMessage('short_greeting', 'Hallo!')

        en_catalog.setMessage('greeting', 'Hello $name, how are you?')
        de_catalog.setMessage('greeting', 'Hallo $name, wie geht es Dir?')

        domain['en-1'] = en_catalog
        domain['de-1'] = de_catalog

        self._view = Translate(domain, self._getRequest())


    def _getRequest(self, **kw):
        environ = kw.pop('environ', {})
        environ['HTTP_HOST'] = 'foo'
        request = BrowserRequest(BytesIO(), environ=environ, **kw)
        request._cookies = {'edit_languages': 'en,de'}
        request._traversed_names = ['foo', 'bar']
        return request


    def testGetMessages(self):
        ids = sorted([m[0] for m in self._view.getMessages()])
        self.assertEqual(ids, ['greeting', 'short_greeting'])


    def testGetTranslation(self):
        self.assertEqual(self._view.getTranslation('short_greeting', 'en'),
                         'Hello!')


    def testGetAllLanguages(self):
        languages = sorted(self._view.getAllLanguages())
        self.assertEqual(languages, ['de', 'en'])


    def testGetEditLanguages(self):
        languages = sorted(self._view.getEditLanguages())
        self.assertEqual(languages, ['de', 'en'])


    def testAddDeleteLanguage(self):
        self._view.addLanguage('es')
        self.assertIn('es', self._view.getAllLanguages())
        self._view.deleteLanguages(['es'])
        self.assertNotIn('es', self._view.getAllLanguages())

    def test_editMessage(self):
        request = self._getRequest(form={
            'msg_id': 'short_greeting',
            'msg_lang_en': 'Howdy',
            'msg_lang_de': 'Guten Tag',
        })
        view = Translate(self._domain, request)
        view.editMessage()
        self.assertEqual(view.getTranslation('short_greeting', 'en'),
                         'Howdy')

    def test_editMessages_add(self):
        request = self._getRequest(form={
            'new-msg_id-1': 'short_greeting2',
            'new-en-1': 'Howdy',
            'new-de-1': 'Guten Tag',
        })
        view = Translate(self._domain, request)
        view.editMessages()
        self.assertEqual(view.getTranslation('short_greeting2', 'en'),
                         'Howdy')

    def test_editMessages_edit(self):
        request = self._getRequest(form={
            'edit-msg_id-1': 'short_greeting',
            'edit-en-1': 'Howdy',
            'edit-de-1': 'Guten Tag',
        })
        view = Translate(self._domain, request)
        view.editMessages()
        self.assertEqual(view.getTranslation('short_greeting', 'en'),
                         'Howdy')

    def test_deleteMessages(self):
        request = self._getRequest(form={
            'edit-msg_id-1': 'short_greeting',
        })
        view = Translate(self._domain, request)
        view.deleteMessages(['1'])
        self.assertEqual(view.getTranslation('short_greeting', 'en'),
                         'short_greeting')

        # idempotent
        view.deleteMessages(['1'])
        self.assertEqual(view.getTranslation('short_greeting', 'en'),
                         'short_greeting')

    def test_changeEditLanguages(self):
        self._view.changeEditLanguages(('en',))
        self.assertEqual({'value': 'en'},
                         self._view.request.response.getCookie('edit_languages'))


    def test_changeFilter(self):
        self._view.changeFilter()
        self.assertEqual({'value': '%'},
                         self._view.request.response.getCookie('filter'))

class TestSynchronize(unittest.TestCase):

    layer = ZCMLFileLayer(zope.app.i18n.tests)


    def setUp(self):
        self._domain = domain = TranslationDomain()
        domain.domain = 'default'

        en_catalog = MessageCatalog('en', 'default')
        de_catalog = MessageCatalog('de', 'default')

        en_catalog.setMessage('short_greeting', 'Hello!')
        de_catalog.setMessage('short_greeting', 'Hallo!')

        en_catalog.setMessage('greeting', 'Hello $name, how are you?')
        de_catalog.setMessage('greeting', 'Hallo $name, wie geht es Dir?')

        domain['en-1'] = en_catalog
        domain['de-1'] = de_catalog

    def _getRequest(self, **kw):
        environ = kw.pop('environ', {})
        environ['HTTP_HOST'] = 'foo'
        request = BrowserRequest(BytesIO(), environ=environ, **kw)
        request._traversed_names = ['foo', 'bar']
        return request

    def test_synchronize_imports(self):
        # Trivial test that imports the module.  This would have triggered a
        # deprecation warning in previous versions.
        import zope.app.i18n.browser.synchronize

    def test_create_view_cover(self):
        from zope.app.i18n.browser.synchronize import Synchronize
        request = self._getRequest(form={
            'sync_username': 'admin',
            'sync_password': 'admin',
            'message_ids': ['short_greeting'],
            'update-msgid-short_greeting': 'short_greeting',
            'update-language-short_greeting': 'en',
        })
        request._cookies['sync_url'] = 'not a valid domain'
        s = Synchronize(self._domain, request)

        self.assertFalse(s._isConnected())
        s._disconnect()
        self.assertFalse(s.canConnect())

        self.assertEqual([], s.getAllLanguages())
        self.assertEqual({}, s.queryMessages())
        self.assertEqual([], s.queryMessageItems())

        self.assertEqual(u'Does not exist', s.getStatus(None, None))
        self.assertEqual(u'New Remote', s.getStatus({}, None))
        self.assertEqual(u'Out of Date', s.getStatus({'mod_time': 1}, {'mod_time': 0}))
        self.assertEqual(u'Newer Local', s.getStatus({'mod_time': 0}, {'mod_time': 1}))
        self.assertEqual(u'Up to Date', s.getStatus({'mod_time': 1}, {'mod_time': 1}))

        s.saveSettings()
        s.synchronize()
        s.queryMessages = lambda: {('short_greeting', 'en'): [{'mod_time': 0}, {'mod_time': 0}]}
        s.synchronizeMessages()

        del s.queryMessages

        # Now stub out the connection
        class Stub(object):
            def getAllLanguages(self):
                return ('en',)
            def getMessagesFor(self, langs):
                return []
        s._connection = Stub()

        self.assertTrue(s._isConnected())
        self.assertTrue(s.canConnect())
        self.assertEqual(('en',), s.getAllLanguages())
        self.assertEqual({}, s.queryMessages())

    def test_make_url(self):
        from zope.app.i18n.browser.synchronize import Synchronize
        request = self._getRequest(form={
            'sync_username': 'admin',
            'sync_password': 'admin',
            'message_ids': ['short_greeting'],
            'update-msgid-short_greeting': 'short_greeting',
            'update-language-short_greeting': 'en',
        })
        s = Synchronize(self._domain, request)
        self.assertEqual('http://admin:admin@localhost:8080/++etc++site/default/zope',
                         s._make_sync_url())

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main()
