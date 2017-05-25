from django.conf.urls import url
from dpmenu.views.menu_lc import MenuLCAPIView
from dpmenu.views.menu_rud import MenuRUDAPIView

urlpatterns = [
    url(r'^menus/$', MenuLCAPIView.as_view(),name='menu-lc'),
    url(r'^menus/(?P<pk>[0-9]+)/$', MenuRUDAPIView.as_view(), name='menu-rud'),
]
