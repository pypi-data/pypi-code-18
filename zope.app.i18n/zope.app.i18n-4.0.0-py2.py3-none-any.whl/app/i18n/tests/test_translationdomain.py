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
"""This module tests the regular persistent Translation Domain.

"""
import unittest
import doctest

from zope.component import getGlobalSiteManager
from zope.component import provideUtility
from zope.component import provideAdapter
from zope.component.interfaces import IFactory
from zope.component.factory import Factory
from zope.i18n.interfaces import ITranslationDomain

from zope.i18n.tests import test_itranslationdomain
from zope.i18n.translationdomain \
     import TranslationDomain as GlobalTranslationDomain

from zope.interface.verify import verifyObject
from zope.traversing.api import traverse


from zope.app.component.testing import PlacefulSetup
from zope.app.component.testing import createSiteManager


from zope.app.i18n import interfaces
from zope.app.i18n.messagecatalog import MessageCatalog
from zope.app.i18n.translationdomain import TranslationDomain

from zope.site.site import SiteManagerAdapter
from zope.component.interfaces import IComponentLookup
from zope.interface import Interface

def setUpSiteManagerLookup():
    provideAdapter(SiteManagerAdapter, (Interface,),
                   IComponentLookup)


class AbstractTestILocalTranslationDomainMixin(object):

    def testInterface(self):
        verifyObject(ITranslationDomain, self._domain)

    def _getLanguages(self, domain):
        languages = sorted(domain.getAllLanguages())
        return languages

    def testGetAddDeleteLanguage(self):
        domain = self._domain
        langs = self._getLanguages(domain)
        domain.addLanguage('es')
        self.assertEqual(self._getLanguages(domain), langs+['es'])
        domain.addLanguage('fr')
        self.assertEqual(self._getLanguages(domain), langs+['es', 'fr'])
        self.assertEqual(domain.getAvailableLanguages(),
                         langs+['es', 'fr'])
        domain.deleteLanguage('es')
        self.assertEqual(self._getLanguages(domain), langs+['fr'])
        domain.deleteLanguage('fr')
        self.assertEqual(self._getLanguages(domain), langs)

    def testAddUpdateDeleteMessage(self):
        domain = self._domain
        self.assertEqual(domain.translate('greeting2', target_language='de'),
                         'greeting2')
        self.assertEqual(domain.translate(
            'greeting2', target_language='de', default=42), 42)
        domain.addMessage('greeting2', 'Hallo!', 'de')
        self.assertEqual(domain.translate('greeting2', target_language='de'),
                         'Hallo!')
        domain.updateMessage('greeting2', 'Hallo Ihr da!', 'de')
        self.assertEqual(domain.translate('greeting2', target_language='de'),
                         'Hallo Ihr da!')
        domain.deleteMessage('greeting2', 'de')
        self.assertEqual(domain.translate('greeting2', target_language='de'),
                         'greeting2')


# A test mixing -- don't add this to the suite
class AbstractTestISyncTranslationDomainMixin(object):

    foreign_messages = [
        # Message that is not locally available
        {'domain': 'default', 'language': 'en', 'msgid': 'test',
         'msgstr': 'Test', 'mod_time': 0},
        # This message is newer than the local one.
        {'domain': 'default', 'language': 'de', 'msgid': 'short_greeting',
         'msgstr': 'Hallo.', 'mod_time': 20},
        # This message is older than the local one.
        {'domain': 'default', 'language': 'en', 'msgid': 'short_greeting',
         'msgstr': 'Hello', 'mod_time': 0},
        # This message is up-to-date.
        {'domain': 'default', 'language': 'en', 'msgid': 'greeting',
         'msgstr': 'Hello $name, how are you?', 'mod_time': 0}]


    local_messages = [
        # This message is older than the foreign one.
        {'domain': 'default', 'language': 'de', 'msgid': 'short_greeting',
         'msgstr': 'Hallo!', 'mod_time': 10},
        # This message is newer than the foreign one.
        {'domain': 'default', 'language': 'en', 'msgid': 'short_greeting',
         'msgstr': 'Hello!', 'mod_time': 10},
        # This message is up-to-date.
        {'domain': 'default', 'language': 'en', 'msgid': 'greeting',
         'msgstr': 'Hello $name, how are you?', 'mod_time': 0},
        # This message is only available locally.
        {'domain': 'default', 'language': 'de', 'msgid': 'greeting',
         'msgstr': 'Hallo $name, wie geht es Dir?', 'mod_time': 0},
        ]


    def testInterface(self):
        verifyObject(interfaces.ISyncTranslationDomain, self._domain)
        super(AbstractTestISyncTranslationDomainMixin, self).testInterface()

    def testGetMessagesMapping(self):
        mapping = self._domain.getMessagesMapping(['de', 'en'],
                                                  self.foreign_messages)
        self.assertEqual(mapping[('test', 'en')],
                         (self.foreign_messages[0], None))
        self.assertEqual(mapping[('short_greeting', 'de')],
                         (self.foreign_messages[1], self.local_messages[0]))
        self.assertEqual(mapping[('short_greeting', 'en')],
                         (self.foreign_messages[2], self.local_messages[1]))
        self.assertEqual(mapping[('greeting', 'en')],
                         (self.foreign_messages[3], self.local_messages[2]))
        self.assertEqual(mapping[('greeting', 'de')],
                         (None, self.local_messages[3]))


    def testSynchronize(self):
        domain = self._domain
        mapping = domain.getMessagesMapping(['de', 'en'], self.foreign_messages)
        domain.synchronize(mapping)

        self.assertEqual(domain.getMessage('test', 'en'),
                         self.foreign_messages[0])
        self.assertEqual(domain.getMessage('short_greeting', 'de'),
                         self.foreign_messages[1])
        self.assertEqual(domain.getMessage('short_greeting', 'en'),
                         self.local_messages[1])
        self.assertEqual(domain.getMessage('greeting', 'en'),
                         self.local_messages[2])
        self.assertEqual(domain.getMessage('greeting', 'en'),
                         self.foreign_messages[3])
        self.assertEqual(domain.getMessage('greeting', 'de'),
                         None)


class TestTranslationDomain(
        AbstractTestISyncTranslationDomainMixin,
        AbstractTestILocalTranslationDomainMixin,
        test_itranslationdomain.TestITranslationDomain,
        unittest.TestCase):

    def setUp(self):
        # placefulSetup
        psetup = PlacefulSetup()
        self.sm = psetup.setUp(True, True)
        self.rootFolder = psetup.rootFolder

        super(TestTranslationDomain, self).setUp()
        setUpSiteManagerLookup()

        self.sm.registerUtility(self._domain, ITranslationDomain, 'default')

        provideUtility(Factory(MessageCatalog), IFactory,
                       'zope.app.MessageCatalog')

    def tearDown(self):
        PlacefulSetup().tearDown()

    def _getTranslationDomain(self):
        domain = TranslationDomain()
        domain.domain = 'default'

        en_catalog = MessageCatalog('en', 'default')
        de_catalog = MessageCatalog('de', 'default')
        # Populate the catalogs with translations of a message id
        en_catalog.setMessage('short_greeting', 'Hello!', 10)
        de_catalog.setMessage('short_greeting', 'Hallo!', 10)
        # And another message id with interpolation placeholders
        en_catalog.setMessage('greeting', 'Hello $name, how are you?', 0)
        de_catalog.setMessage('greeting', 'Hallo $name, wie geht es Dir?', 0)

        domain['en-1'] = en_catalog
        domain['de-1'] = de_catalog

        return domain

    def testParameterNames(self):
        # Test that the second argument is called `msgid'
        self.assertEqual(
            self._domain.translate('short_greeting', target_language='en'),
            'Hello!')

    def testCatalogDomain(self):
        domain = self._domain
        domain.domain = 'myfault'
        domain.addMessage('greeting2', 'Hola!', 'ca')
        self.assertEqual(domain['ca'].domain, domain.domain)
        domain.domain = 'default'

    def test_getMessages(self):
        messages = [{'domain': 'default',
                     'language': 'de',
                     'mod_time': 0,
                     'msgid': 'greeting',
                     'msgstr': 'Hallo $name, wie geht es Dir?'},
                    {'domain': 'default',
                     'language': 'de',
                     'mod_time': 10,
                     'msgid': 'short_greeting',
                     'msgstr': 'Hallo!'},
                    {'domain': 'default',
                     'language': 'en',
                     'mod_time': 0,
                     'msgid': 'greeting',
                     'msgstr': 'Hello $name, how are you?'},
                    {'domain': 'default',
                     'language': 'en',
                     'mod_time': 10,
                     'msgid': 'short_greeting',
                     'msgstr': 'Hello!'}]
        self.assertEqual(messages,
                         self._domain.getMessages())

class TestTranslationDomainInAction(unittest.TestCase):

    def setUp(self):
        psetup = PlacefulSetup()
        self.sm = psetup.setUp(True, True)
        self.rootFolder = psetup.rootFolder
        setUpSiteManagerLookup()

        import zope.i18n.interfaces
        import zope.i18n.negotiator
        provideUtility(zope.i18n.negotiator.negotiator,
                       zope.i18n.interfaces.INegotiator)


        gsm = getGlobalSiteManager()
        de_catalog = MessageCatalog('de', 'default')
        de_catalog.setMessage('short_greeting', 'Hallo!', 10)
        de_catalog.setMessage('long_greeting', 'Guten Tag!', 10)

        # register global translation domain and add the catalog.
        domain = GlobalTranslationDomain('default')
        domain.addCatalog(de_catalog)
        gsm.registerUtility(domain, ITranslationDomain, 'default')

        # create a local site manager and add a local translation domain
        td = TranslationDomain()
        td.domain = 'default'
        de_catalog = MessageCatalog('de', 'default')
        de_catalog.setMessage('short_greeting', 'Hallo Welt!', 10)
        td['de-default-1'] = de_catalog

        mgr = createSiteManager(traverse(self.rootFolder, 'folder1'))
        mgr['default']['default'] = td
        mgr.registerUtility(mgr['default']['default'], ITranslationDomain, 'default')

        self.trans1 = td
        self.trans = domain

    def tearDown(self):
        PlacefulSetup().tearDown()

    def test_translate(self):
        self.assertEqual(
            self.trans.translate('short_greeting', context='default',
                                 target_language='de'),
            'Hallo!')
        self.assertEqual(
            self.trans1.translate('short_greeting', context='default',
                                  target_language='de'),
            'Hallo Welt!')

        self.assertEqual(
            self.trans1.translate('long_greeting', context='default',
                                  target_language='de'),
            'Guten Tag!')

def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        doctest.DocTestSuite('zope.app.i18n.translationdomain'),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
