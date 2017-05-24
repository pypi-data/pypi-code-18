#!/usr/lib/env python
# -*- encoding:utf-8 -*-

import os
import sys
import tornado.web


class route(object):
    """
        @route('/some/path')
        class SomeRequestHandler(RequestHandler):
            pass

        @route('/some/path', name='other')
        class SomeOtherRequestHandler(RequestHandler):
            pass
        
        routes = route.get_routes()
    """
    _routes = []

    def __init__(self, uri, name=None):
        self._uri = uri
        self.name = name

    
    def __call__(self, _handler):
        name = self.name and self.name or _handler.__name__
        self._routes.append(tornado.web.url(self._uri, _handler, name=name))
        return _handler


    @classmethod
    def get_routes(self, path = "."):
        scan_handlers(path)
        return route._routes
    
    
def scan_handlers(path = "."):
    """
        扫描
    """
    path = os.path.abspath(path)
    if not os.path.exists(path):
        return

    for p in os.listdir(path):
        if os.path.exists(os.path.join(path, p, "__init__.py")):
            scan_handlers(p)
        elif p.endswith(".py") or p.endswith(".pyc"):
            sys.path.insert(0, os.path.dirname(os.path.join(path, p)))
            __import__(os.path.splitext(p)[0])
            sys.path.remove(sys.path[0])
