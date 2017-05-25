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
"""This module tests the Gettext Export and Import funciotnality of the
Translation Domain.

"""
import unittest
import time
from io import BytesIO


from zope.component.testing import PlacelessSetup
from zope.component.interfaces import IFactory
from zope.component.factory import Factory
from zope.component import provideUtility

from zope.app.i18n.messagecatalog import MessageCatalog
from zope.i18n.negotiator import negotiator
from zope.i18n.interfaces import INegotiator

from zope.app.i18n.translationdomain import TranslationDomain
from zope.app.i18n.filters import GettextImportFilter
from zope.app.i18n.filters import GettextExportFilter
from zope.app.i18n.filters import ParseError
from zope.app.i18n.filters import parseGetText

GETTEXT_IMPORT_DATA = b'''

msgid ""
msgstr ""
"Project-Id-Version: Zope 3\\n"
"PO-Revision-Date: %s\\n"
"Last-Translator: Zope 3 Gettext Export Filter\\n"
"Zope-Language: de\\n"
"Zope-Domain: default\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Choose"
# comment
msgstr "Ausw\xc3\xa4hlen!"
# comment

# comment
msgid "greeting"
msgstr "hallo"
# comment
'''

class TestGettextExportImport(PlacelessSetup, unittest.TestCase):

    _data = GETTEXT_IMPORT_DATA

    def setUp(self):
        super(TestGettextExportImport, self).setUp()

        # Setup the negotiator utility
        provideUtility(negotiator, INegotiator)

        self._domain = TranslationDomain()
        self._domain.domain = 'default'
        provideUtility(Factory(MessageCatalog), IFactory,
                       'zope.app.MessageCatalog')

    def testImportExport(self):
        imp = GettextImportFilter(self._domain)
        # Insert some extra lines and comments for the parser to skip
        import_data = b'\n\n'.join(self._data.split(b'\n'))

        imp.importMessages(['de'],
                           BytesIO(import_data % b'2002/02/02 02:02'))

        exp = GettextExportFilter(self._domain)
        result = exp.exportMessages('de')

        dt = time.time()
        dt = time.localtime(dt)
        dt = time.strftime('%Y/%m/%d %H:%M', dt)
        if not isinstance(dt, bytes):
            dt = dt.encode("utf-8")

        expected = self._data.replace(b'# comment\n', b'') % dt
        self.assertEqual(result.strip(), expected.strip())

    def test_bad_export_argument(self):
        exp = GettextExportFilter(self._domain)
        self.assertRaises(TypeError, exp.exportMessages, ['1', '2'])

class TestParseGetText(unittest.TestCase):

    def setUp(self):
        self._domain = TranslationDomain()
        super(TestParseGetText, self).setUp()

    def _check_error(self, data, state):
        with self.assertRaises(ParseError) as exc:
            parseGetText(data)

        self.assertEqual(exc.exception.state, state)


    def test_bad_start_state(self):
        data = [b'bad first line']
        self._check_error(data, 0)

    def test_bad_state_after_comment(self):
        data = [b'# comment', b'bad state']
        self._check_error(data, 1)

    def test_bad_state_after_id(self):
        data = [b'msgid ""', b'bad state']
        self._check_error(data, 2)

    def test_bad_state_after_str(self):
        data = [b'msgid ""', b'msgstr ""', b'bad state']
        self._check_error(data, 3)

    def test_multiline_msgid(self):
        data = [b'msgid "a"', b'"b"', b'msgstr ""']
        _, ids, _, _ = parseGetText(data)
        self.assertEquals(ids, [b'a', b'b'])

class TestParseError(unittest.TestCase):

    def test_str(self):
        error = ParseError("state", 10, 'data')
        self.assertEqual("state state, line num 10: 'data'", str(error))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
