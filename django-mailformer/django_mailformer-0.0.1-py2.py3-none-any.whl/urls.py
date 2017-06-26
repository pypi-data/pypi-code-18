# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from .constants import URL_NAME

urlpatterns = [
    url(r'^$', views.EmailFormView.as_view(), name=URL_NAME['form']),
    url(r'success/$', views.EmailFormSuccessView.as_view(), name=URL_NAME['success']),
]
