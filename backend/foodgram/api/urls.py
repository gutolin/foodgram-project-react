from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FollowViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet, UserViewSet)

app_name = 'api'

routers_v1 = DefaultRouter()
routers_v1.register(r'users', UserViewSet, basename='users')
routers_v1.register(r'tags', TagViewSet, basename='tags')
routers_v1.register(r'recipes', RecipeViewSet, basename='recipes')
routers_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
routers_v1.register(r'users/subscriptions', FollowViewSet,
                    basename='subscriptions')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(routers_v1.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls.authtoken')),
]
