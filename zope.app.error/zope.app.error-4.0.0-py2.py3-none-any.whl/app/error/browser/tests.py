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


from zope.component.testlayer import ZCMLFileLayer
from zope.publisher.interfaces.http import IHTTPRequest
from zope.interface import implementer

import zope.app.error.browser
from zope.app.error.browser import EditErrorLog
from zope.app.error.browser import ErrorRedirect

class TestEditErrorLog(unittest.TestCase):

    def test_updateProperties(self):
        class Context(object):
            props = None
            def setProperties(self, keep_entries, copy_to_zlog, ignored_exceptions):
                self.props = dict(locals())
                del self.props['self']

        class Request(object):
            url = None
            @property
            def response(self):
                return self
            def redirect(self, url):
                self.url = url

        edit = EditErrorLog()
        edit.context = Context()
        edit.request = Request()
        edit.updateProperties('keep')

        self.assertEqual(edit.context.props,
                         {'copy_to_zlog': 0,
                          'ignored_exceptions': None,
                          'keep_entries': 'keep'})
        self.assertEqual(edit.request.url, '@@configure.html')

class TestErrorRedirect(unittest.TestCase):

    layer = ZCMLFileLayer(zope.app.error.browser,
                          name='AppErrorLayer')

    def test_action_type_error(self):

        @implementer(IHTTPRequest)
        class Request(object):
            url = None

            @property
            def response(self):
                return self

            def getVirtualHostRoot(self):
                return None

            def getApplicationURL(self):
                return 'http://localhost'

            def redirect(self, url):
                self.url = url

        redirect = ErrorRedirect(None, Request())
        redirect.action()

        self.assertEqual(redirect.request.url,
                         'http://localhost/@@errorRedirect.html')

    def test_action_no_type_error(self):
        from zope.component import getUtility
        from zope.error.interfaces import IErrorReportingUtility

        @implementer(IHTTPRequest)
        class Request(object):
            url = None

            @property
            def response(self):
                return self

            root = None
            def getVirtualHostRoot(self):
                return self.root

            def getApplicationURL(self):
                return 'http://localhost'

            def redirect(self, url):
                self.url = url

        redirect = ErrorRedirect(None, Request())
        redirect.request.root = getUtility(IErrorReportingUtility)
        redirect.action()

        self.assertEqual(redirect.request.url,
                         'http://localhost/@@SelectedManagementView.html')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
