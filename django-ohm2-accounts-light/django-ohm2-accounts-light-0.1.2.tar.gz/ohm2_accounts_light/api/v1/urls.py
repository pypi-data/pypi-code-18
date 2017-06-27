from django.conf.urls import url
from . import views



urlpatterns = [
	url(r'^signup/$', views.signup, name = 'signup'),
	url(r'^login/$', views.login, name = 'login'),
	url(r'^logout/$', views.logout, name = 'logout'),
	url(r'^signup-and-get-token/$', views.signup_and_get_token, name = 'signup_and_get_token'),
	url(r'^login-and-get-token/$', views.login_and_get_token, name = 'login_and_get_token'),
]


urlpatterns += [
	url(r'^send-password-reset-link/$', views.send_password_reset_link, name = 'send_password_reset_link'),
	url(r'^set-password-reset/$', views.set_password_reset, name = 'set_password_reset'),
	url(r'^set-password-reset-and-get-token/$', views.set_password_reset_and_get_token, name = 'set_password_reset_and_get_token'),
	url(r'^update-user-information/$', views.update_user_information, name = 'update_user_information'),
]