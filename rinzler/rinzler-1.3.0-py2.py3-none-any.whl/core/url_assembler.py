from django.conf.urls import url

from rinzler.core.router import Router


class UrlAssembler(object):

    @staticmethod
    def mount(route, callback):
        return url(r'{0}'.format(route), Router(route, callback).route)
