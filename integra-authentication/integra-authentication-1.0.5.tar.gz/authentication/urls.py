# Author : Partha
"""
    Relative Imports helps us to integrate in any app
"""
from django.conf.urls import url
from .views import user_login, user_register, user_logout

urlpatterns = [
    url(r'^auth/login/$', user_login),
    url(r'^auth/register/$', user_register),  
    url(r'^auth/logout/$', user_logout),  
]
