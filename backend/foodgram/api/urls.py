from django.urls import include, path
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from api.views import TagViewSet, IngredientViewSet, RecipeViewSet

app_name = 'api'

routers_v1 = DefaultRouter()
routers_v1.register(r'tags', TagViewSet, basename='tags')
routers_v1.register(r'recipes', RecipeViewSet, basename='recipes')
routers_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(routers_v1.urls)),
    path('admin/', admin.site.urls),
    # path('auth/signup/', signup, name="signup"),
]
