from rest_framework import filters, viewsets
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from api.models import Recipe, Ingredient, IngredientAmount, Tag, Follow

from .serializers import (TagSerializers,
                          IngredientSerializers,
                          RecipeSerializers,
                          IngredientAmount,
                          )

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializers
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
    pagination_class = None
