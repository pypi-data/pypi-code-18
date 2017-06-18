from inspect import isclass

from flask import Flask as App


def is_provider(service):
    return isclass(service) and issubclass(service, Provider)


def register(app, *services):
    for service in services:
        if is_provider(service):
            service.register(app)
        elif hasattr(service, 'init_app'):
            service.init_app(app)
        else:
            service(app)

    for service in services:
        if is_provider(service):
            service.boot(app)


class Provider(object):

    def register(app):
        pass

    def boot(app):
        pass
