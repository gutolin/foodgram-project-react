from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from api.models import Recipe, Ingredient, IngredientAmount, Tag, Follow

from .serializers import (TagSerializers,
                          IngredientSerializers,
                          RecipeSerializers,
                          IngredientAmount
                          )

#class CategoryViewSet(viewsets.ModelViewSet):
#    queryset = Categories.objects.all()
#    serializer_class = CategorySerializers
#    filter_backends = (filters.SearchFilter,)
#    search_fields = ('name',)
#    permission_classes = [IsAdminUserOrReadOnly]
#    pagination_class = PageNumberPagination
#    lookup_field = 'slug'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializers
    pagination_class = PageNumberPagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmount


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
