# Author : Partha
"""
    Relative Imports helps us to integrate with any app
"""
from django.conf.urls import url
from .views import list_creds, add_creds, edit_creds

urlpatterns = [
    url(r'^setup/creds/search/$', list_creds),
    url(r'^setup/creds/add/$', add_creds),  
    url(r'^setup/creds/edit/(?P<pk>[\w-]+)/$', edit_creds),  
]
