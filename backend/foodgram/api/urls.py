from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipeViewSet,
                       TagViewSet, CustomUserViewSet)

app_name = 'api'

routers_v1 = DefaultRouter()
routers_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
routers_v1.register(r'tags', TagViewSet, basename='tags')
routers_v1.register(r'recipes', RecipeViewSet, basename='recipes')
routers_v1.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(routers_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
