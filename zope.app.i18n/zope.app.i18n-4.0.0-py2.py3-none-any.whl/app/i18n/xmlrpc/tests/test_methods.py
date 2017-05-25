##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
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
import unittest

from zope.app.i18n.translationdomain import TranslationDomain
from zope.app.i18n.messagecatalog import MessageCatalog

from zope.app.i18n.xmlrpc.methods import Methods
from zope.publisher.browser import TestRequest

class TestMethods(unittest.TestCase):

    def setUp(self):
        super(TestMethods, self).setUp()

        domain = self._domain = TranslationDomain()
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


    def testMethods(self):
        view = Methods(self._domain, TestRequest())

        self.assertEqual(['de', 'en'], view.getAllLanguages())

        self.assertEqual([], view.getMessagesFor([]))

        self.assertEqual([{'domain': 'default',
                           'language': 'en',
                           'mod_time': 0,
                           'msgid': 'greeting',
                           'msgstr': 'Hello $name, how are you?'},
                          {'domain': 'default',
                           'language': 'en',
                           'mod_time': 10,
                           'msgid': 'short_greeting',
                           'msgstr': 'Hello!'}],
                         view.getMessagesFor(['en']))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


if __name__ == '__main__':
    unittest.main(defaultTest=test_suite)
