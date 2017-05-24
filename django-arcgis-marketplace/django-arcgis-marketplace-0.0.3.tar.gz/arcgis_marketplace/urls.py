from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(
        template_name='arcgis_marketplace/index.html')),

    url(r'^items/(?P<pk>[0-9a-f]{32})/paypal-form$',
        views.ItemPaypalFormView.as_view(),
        name='item-paypal-form'),

    url(r'^api/', include(
        'arcgis_marketplace.api.urls',
        namespace='api'))
]
