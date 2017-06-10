from django.conf.urls import url

from . import views

app_name = 'jobs'
urlpatterns = [
    url(r'^$', views.get_jobs, name='list'),
    url(r'^submit/', views.submit_job, name='submit'),
    url(r'^(?P<jobsubmitted_id>[0-9]+)/$', views.get_job_detail, name='detail'),
    url(r'^profile/', views.edit_profile, name='profile'),
    url(r'^create_user/', views.create_new_user, name='new-user'),
    #url(r'^(?P<jobsubmitted_id>[0-9]+)/note/$', views.get_job_note, name='note'),
]
