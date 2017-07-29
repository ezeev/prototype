from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views, api_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^status/$', views.status, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),
    url(r'^api/status/$', api_views.api_status, name='status-api'),
    url(r'^api/query/$', api_views.api_query, name='query-api'),
]