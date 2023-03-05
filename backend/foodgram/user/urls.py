from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

app_name = 'user'

routers_v1 = DefaultRouter()
routers_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(routers_v1.urls)),
    path('', include('djoser.urls')),
]
