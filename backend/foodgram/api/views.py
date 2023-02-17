from api.models import Follow, Ingredient, IngredientAmount, Recipe, Tag
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import filters, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import (FollowSerializers, IngredientAmountSerializers,
                          IngredientSerializers, RecipeSerializers,
                          TagSerializers, RecipeSubscriberSerializers)

from api.filters import RcipesFilter
from api.models import Favorites

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializers
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_class = RcipesFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user

        if request.method == 'POST':
            if Favorites.objects.filter(user=user, recipe__id=pk).exists():
                return Response({
                    'errors': 'Рецепт уже добавлен в список'
                }, status=status.HTTP_400_BAD_REQUEST)

            recipe = get_object_or_404(Recipe, pk=pk)
            Favorites.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubscriberSerializers(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            obj = Favorites.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален'
            }, status=status.HTTP_400_BAD_REQUEST)

        return None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializers


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.ListModelMixin, viewsets.GenericViewSet):

    pass


class FollowViewSet(CreateRetrieveViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )