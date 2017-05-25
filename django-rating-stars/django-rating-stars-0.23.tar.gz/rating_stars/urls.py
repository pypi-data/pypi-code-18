# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import UpdateRatingView


urlpatterns = [
    url(r'^$', UpdateRatingView.as_view(), name='update_rating'),
]
