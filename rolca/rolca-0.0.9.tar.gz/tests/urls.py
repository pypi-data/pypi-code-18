"""Test project's urls."""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^', include('rolca.urls')),
]
