from django.conf.urls import url
from dpuser.views.user_lc import UserLCAPIView
from dpuser.views.user_rud import UserRUDAPIView

urlpatterns = [
    url(r'^users/$', UserLCAPIView.as_view(),name='user-list-create'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserRUDAPIView.as_view(), name='user-retrieve-update-delete'),
]
