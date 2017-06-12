""".. Ignore pydocstyle D400.

=========
Core URLs
=========

"""
from django.conf.urls import url

from . import views


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^contest/(?P<contest_id>\d+)/download$', views.download_contest, name="download-contest")
]
