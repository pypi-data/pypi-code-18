from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from dpauth.views.signup import SignupAPIView


urlpatterns = [
    url(r'^login/', obtain_jwt_token, name='auth-login'),
    url(r'^signup/', SignupAPIView.as_view(), name='auth-signup'),
    url(r'^verify-token/', verify_jwt_token, name='verify-token'),
    url(r'^refresh-token/', refresh_jwt_token, name='refresh-token'),
]
