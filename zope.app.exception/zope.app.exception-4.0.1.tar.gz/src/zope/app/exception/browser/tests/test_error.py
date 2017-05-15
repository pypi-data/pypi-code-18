##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""Functional tests for NotFoundError
"""
import doctest
import unittest
from zope.component.interfaces import ComponentLookupError
from zope.app.exception.testing import AppExceptionLayer
from zope.app.exception.browser.tests import BrowserTestCase
from zope.app.wsgi.testlayer import http

class RaiseError(object):

    def __call__(self):
        raise Exception()


class RaiseComponentLookupError(object):

    def __call__(self):
        raise ComponentLookupError()


class TestComponentLookupError(BrowserTestCase):

    layer = AppExceptionLayer

    def testComponentLookupError(self):
        response = self.publish('/foobar', basic='mgr:mgrpw',
                                handle_errors=True)
        self.assertEqual(response.status_int, 404)
        body = response.unicode_normal_body
        self.assertIn(
            'The page that you are trying to access is not available', body)

class TestMisc(unittest.TestCase):

    def test_user(self):
        from zope.app.exception.browser import user
        view = user.UserErrorView()
        view.context = self
        self.assertEqual(view.title(), self.__class__.__name__)

    def test_interfaces(self):
        from zope.app.exception import interfaces
        from zope.browser.interfaces import ISystemErrorView
        self.assertEqual(interfaces.ISystemErrorView, ISystemErrorView)

class TestUserpt(unittest.TestCase):

    layer = AppExceptionLayer

    def _render_with_context(self, context):
        from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
        from zope.publisher.browser import TestRequest
        import os
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'user.pt')

        template = ViewPageTemplateFile(path)

        class Instance(object):
            def __init__(self):
                self.context = context
                self.request = TestRequest()
                self.request.setPrincipal(self)

            title = 'principal'

        instance = Instance()

        return template(instance)

    def test_render_with_exception(self):
        s = self._render_with_context(Exception("This is the message"))
        self.assertIn("This is the message", s)

    def test_render_with_iterable(self):
        s = self._render_with_context(["Just an iterable"])
        self.assertIn("Just an iterable", s)


def test_suite():
    TestComponentLookupError.layer = AppExceptionLayer

    def _http(query_str, *args, **kwargs):
        wsgi_app = AppExceptionLayer.make_wsgi_app()
        # Strip leading \n
        query_str = query_str.lstrip()
        kwargs.setdefault('handle_errors', True)
        if not isinstance(query_str, bytes):
            query_str = query_str.encode("utf-8")
        return http(wsgi_app, query_str, *args, **kwargs)


    systemerror = doctest.DocFileSuite(
        '../systemerror.rst',
        optionflags=doctest.ELLIPSIS,
        globs={'http': _http})

    systemerror.layer = AppExceptionLayer
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        systemerror,
    ))
