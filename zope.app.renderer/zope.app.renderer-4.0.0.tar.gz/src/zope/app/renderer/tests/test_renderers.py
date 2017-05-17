##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Renderer Tests

"""
import unittest
import doctest
from doctest import DocTestSuite

def test_suite():
    options = doctest.ELLIPSIS
    return unittest.TestSuite((
        DocTestSuite('zope.app.renderer.plaintext'),
        DocTestSuite('zope.app.renderer.rest'),
        DocTestSuite('zope.app.renderer.stx',
                     optionflags=options),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
