from django.conf.urls import url
from .views import session_list_view, sign_out_other_view


urlpatterns = [
    url(r"^$", session_list_view, name="session_activity_list"),
    url(r"^sign-out-other/", sign_out_other_view, name="session_sign_out"),
]
