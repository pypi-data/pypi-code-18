import re

from .controllers import Controller
from .helpers import findclass, before, after


class Route(object):
    methods = ['get', 'head', 'post', 'put', 'patch', 'delete', 'options']

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = '/' + prefix

    def group(self, **keywords):
        return self.__class__(self.app, **keywords)

    def any(self, handler, *urls, **keywords):
        if 'endpoint' not in keywords:
            keywords['endpoint'] = handler.__qualname__

        cls = findclass(handler)
        if cls is not None and issubclass(cls, Controller):
            obj = cls(self.app)
            handler = getattr(obj, handler.__name__)
            if hasattr(obj, 'before'):
                handler = before(obj.before)(handler)
            if hasattr(obj, 'after'):
                handler = after(obj.after)(handler)

        for url in urls:
            url = '/'.join([self.prefix, url])
            url = re.sub('[\/]+', '/', url)
            self.app.add_url_rule(url, view_func=handler, **keywords)

        return self

    def __getattr__(self, name):
        if name not in self.methods:
            raise AttributeError(name)

        def func(*arguments, **keywords):
            if 'methods' not in keywords:
                keywords['methods'] = [name.upper()]

            self.any(*arguments, **keywords)

        return func

    def resource(self, Resource, *arguments, **keywords):
        resource = Resource(self.app)
        for method in self.methods:
            if hasattr(resource, method):
                route = getattr(self, method)
                handler = getattr(resource, method)
                route(handler, *arguments, **keywords)
