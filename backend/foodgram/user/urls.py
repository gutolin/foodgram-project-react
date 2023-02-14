from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import UserViewSet

app_name = 'user'

routers_v1 = DefaultRouter()
routers_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(routers_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
