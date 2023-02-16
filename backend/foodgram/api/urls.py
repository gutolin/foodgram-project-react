from api.views import (FollowViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet)
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

routers_v1 = DefaultRouter()
routers_v1.register(r'tags', TagViewSet, basename='tags')
routers_v1.register(r'recipes', RecipeViewSet, basename='recipes')
routers_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
routers_v1.register(r'users/subscriptions', FollowViewSet,
                    basename='subscriptions')
#routers_v1.register(r'users/(?P<id>\d+)/subscribe', FollowViewSet,
#                    basename='subscribe')

urlpatterns = [
    path('', include(routers_v1.urls)),
    path('admin/', admin.site.urls),
]
