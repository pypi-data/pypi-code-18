""".. Ignore pydocstyle D400.

=============
Frontend URLs
=============

"""
from django.conf.urls import url
from django.views.generic.base import RedirectView

from rolca.frontend import views

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^upload/$', views.select_contest_view, name="select_contest"),
    url(r'^upload/(?P<contest_id>\d+)$', views.upload_view, name="upload"),
    url(r'^confirm$', views.confirm_view, name="upload_confirm"),
    url(r'', RedirectView.as_view(pattern_name='rolca-frontend:select_contest')),

    # url(r'^seznam$', 'uploader.views.list_select', name="list_select"),
    # url(r'^seznam/(?P<contest_id>\d+)$', 'uploader.views.list_details',
    #     name="list_datails"),

]
