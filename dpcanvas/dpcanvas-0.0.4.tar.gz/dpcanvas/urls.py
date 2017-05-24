from django.conf.urls import url
from dpcanvas.views.canvas_lc import CanvasLCAPIView
from dpcanvas.views.canvas_rud import CanvasRUDAPIView

urlpatterns = [
    url(r'^canvas/$', CanvasLCAPIView.as_view(),name='canvas-lc'),
    url(r'^canvas/(?P<pk>[0-9]+)/$', CanvasRUDAPIView.as_view(), name='canvas-rud'),
]
