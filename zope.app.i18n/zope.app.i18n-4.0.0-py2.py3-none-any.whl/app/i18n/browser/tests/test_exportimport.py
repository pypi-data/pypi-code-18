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
"""This module tests the Gettext Export and Import funciotnality of the
Translation Domain.

"""
import unittest
import time
from io import BytesIO

from zope.component.testlayer import ZCMLFileLayer

from zope.app.i18n.translationdomain import TranslationDomain
from zope.app.i18n.browser.exportimport import ExportImport
import zope.app.i18n.tests
from zope.publisher.browser import TestRequest

from zope.app.i18n.tests.test_filters import GETTEXT_IMPORT_DATA

class TestExportImport(unittest.TestCase):

    layer = ZCMLFileLayer(zope.app.i18n.tests)

    data = GETTEXT_IMPORT_DATA

    def setUp(self):
        super(TestExportImport, self).setUp()

        self._domain = TranslationDomain()
        self._domain.domain = 'default'

    def testImportExport(self):
        view = ExportImport()
        view.context = self._domain
        view.request = TestRequest()
        view.request.getURL = lambda _x: 'url'

        # Insert some extra lines and comments for the parser to skip
        import_data = b'\n\n'.join(self.data.split(b'\n'))

        view.importMessages(['de'],
                            BytesIO(import_data % b'2002/02/02 02:02'))

        result = view.exportMessages('de')

        dt = time.time()
        dt = time.localtime(dt)
        dt = time.strftime('%Y/%m/%d %H:%M', dt)
        if not isinstance(dt, bytes):
            dt = dt.encode("utf-8")

        expected = self.data.replace(b'# comment\n', b'') % dt
        self.assertEqual(result.strip(), expected.strip())

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


if __name__ == '__main__':
    unittest.main(defaultTest=test_suite)
