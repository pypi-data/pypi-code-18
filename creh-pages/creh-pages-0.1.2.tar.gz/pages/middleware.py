# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from pages.models.page import Page


class PageRouteMiddleware(object):

    def process_view(self, request):
        url = request.META['PATH_INFO']

        pages = Page.objects.filter()
        if pages.exists():
            pass
        else:
            pass
        return redirect(url)