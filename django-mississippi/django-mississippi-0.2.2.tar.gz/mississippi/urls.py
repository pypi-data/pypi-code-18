from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sitemap.xml/$', views.sitemap),
    url(r'^(?P<slug>[^/]*)/$', views.dispatch),
]
