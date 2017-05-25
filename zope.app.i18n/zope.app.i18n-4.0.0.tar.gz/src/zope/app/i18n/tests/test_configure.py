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
"""Configuration tests.
"""
import unittest

from zope.component.testing import PlacelessSetup
from zope.configuration import xmlconfig

import zope.app.i18n.tests

class TestConfiguration(PlacelessSetup, unittest.TestCase):

    def test_configure(self):
        xmlconfig.file('ftesting.zcml', zope.app.i18n.tests)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
