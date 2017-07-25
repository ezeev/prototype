from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from api import views
from rest_framework.authtoken import views as rest_framework_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token/$', rest_framework_views.obtain_auth_token, name='api-token'),
]