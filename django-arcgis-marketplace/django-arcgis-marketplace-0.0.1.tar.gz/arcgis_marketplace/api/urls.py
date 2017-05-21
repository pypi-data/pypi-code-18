from django.conf.urls import include
from django.conf.urls import url


app_name = 'arcgis_marketplace.api'

urlpatterns = [
    url(r'^(v1/)?', include(
        'arcgis_marketplace.api.v1.urls', namespace='v1')),
]
