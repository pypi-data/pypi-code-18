"""Main project's urls."""
from django.conf.urls import include, url

from rest_framework import routers

from rolca.core.api import urls as core_api_urls


route_lists = [  # pylint: disable=invalid-name
    core_api_urls.routeList
]

router = routers.DefaultRouter()  # pylint: disable=invalid-name
for route_list in route_lists:
    for prefix, viewset in route_list:
        router.register(prefix, viewset)


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^api/', include(router.urls, namespace='rolca-core-api')),
    url(r'^core/', include('rolca.core.urls', namespace='rolca-core')),
    url(r'^', include('rolca.frontend.urls', namespace='rolca-frontend')),
]
