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
"""Test the generic persistent Message Catalog.

"""
import unittest

from zope.component.interfaces import IFactory
from zope.interface.verify import verifyObject
from zope.app.i18n.messagecatalog import MessageCatalog
from zope.app.i18n.interfaces import ILocalMessageCatalog
from zope.i18n.tests import test_imessagecatalog


class TestLocalMessageCatalog(test_imessagecatalog.TestIMessageCatalog):

    def _getMessageCatalog(self):
        catalog = MessageCatalog('en', 'default')
        catalog.setMessage('short_greeting', 'Hello!', 0)
        catalog.setMessage('greeting', 'Hello $name, how are you?', 0)
        return catalog

    def _getUniqueIndentifier(self):
        return ('en', 'default')

    def setUp(self):
        self._catalog = self._getMessageCatalog()

    def testInterface(self):
        verifyObject(ILocalMessageCatalog, self._catalog)
        self.assertEqual((IFactory,),
                         self._catalog.getInterfaces())

    def testGetFullMessage(self):
        catalog = self._catalog
        self.assertEqual(catalog.getFullMessage('short_greeting'),
                         {'domain': 'default',
                          'language': 'en',
                          'msgid': 'short_greeting',
                          'msgstr': 'Hello!',
                          'mod_time': 0})

    def testSetMessage(self):
        catalog = self._catalog
        catalog.setMessage('test', 'Test', 1)
        self.assertEqual(catalog.getFullMessage('test'),
                         {'domain': 'default',
                          'language': 'en',
                          'msgid': 'test',
                          'msgstr': 'Test',
                          'mod_time': 1})
        catalog.deleteMessage('test')

    def testDeleteMessage(self):
        catalog = self._catalog
        self.assertEqual(catalog.queryMessage('test'), None)
        catalog.setMessage('test', 'Test', 1)
        self.assertEqual(catalog.queryMessage('test'), 'Test')
        catalog.deleteMessage('test')
        self.assertEqual(catalog.queryMessage('test'), None)

    def testGetMessageIds(self):
        catalog = self._catalog
        ids = catalog.getMessageIds()
        ids.sort()
        self.assertEqual(ids, ['greeting', 'short_greeting'])

    def testGetMessages(self):
        catalog = self._catalog
        ids = catalog.getMessageIds()
        ids.sort()
        self.assertEqual(ids, ['greeting', 'short_greeting'])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
