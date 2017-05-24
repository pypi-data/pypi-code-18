from django.conf.urls import url
from dpprogram.views.program_lc import ProgramLCAPIView
from dpprogram.views.program_rud import ProgramRUDAPIView

urlpatterns = [
    url(r'^programs/$', ProgramLCAPIView.as_view(),name='program-lc'),
    url(r'^programs/(?P<pk>[0-9]+)/$', ProgramRUDAPIView.as_view(), name='program-rud'),
]
