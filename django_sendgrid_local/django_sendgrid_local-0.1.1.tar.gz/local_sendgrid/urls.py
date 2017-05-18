""" this document defines the cases app urls """
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'local_sendgrid.views',
    url(
        r'^events/$',
        'events',
        name='django_sendgrid_event'
    )
)
