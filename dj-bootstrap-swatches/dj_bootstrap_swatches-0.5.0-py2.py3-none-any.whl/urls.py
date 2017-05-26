# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(
        r'3',
        TemplateView.as_view(
            template_name="dj_bootstrap_swatches/3.html"
        )
    ),
]
