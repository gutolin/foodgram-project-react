from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import token, UserViewSet

app_name = 'user'

routers_v1 = DefaultRouter()
routers_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(routers_v1.urls)),
    path('auth/token/login/', token, name='auth_token')
]
