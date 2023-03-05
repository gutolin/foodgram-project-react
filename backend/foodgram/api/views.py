from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import (FollowSerializers, IngredientAmountSerializers,
                          IngredientSerializers, RecipeCreateSerializers,
                          RecipeSerializers, RecipeSubscriberSerializers,
                          TagSerializers, UserSerializer)
from api.filters import RecipesFilterSet, IngredientSearchFilter
from api.permissions import IsAdminAuthorOrReadOnly
from recipe.models import (Cart, Favorites, Follow, Ingredient,
                           IngredientAmount, Recipe, Tag)

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюха рецептов.
    пагинация с возможностью установки лимита
    фильтрация по автору, тегу, в избранном, в корзине
    safe методы доустпны любому пользователю."""
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Получение сериализатора для разных методов запросов."""
        if self.action == 'list':
            return RecipeSerializers
        return RecipeCreateSerializers

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Функция для обработки запросов
        на добавление/удаление из избранного."""
        user = request.user

        if request.method == 'POST':
            if Favorites.objects.filter(user=user, recipe__id=pk).exists():
                return Response({
                    'errors': 'Рецепт уже добавлен в избранное'
                }, status=status.HTTP_400_BAD_REQUEST)

            recipe = get_object_or_404(Recipe, pk=pk)
            Favorites.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubscriberSerializers(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            obj = Favorites.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален'
            }, status=status.HTTP_400_BAD_REQUEST)

        return None

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Функция скачивания списка покупок.
        При одинаковых ингредиентов в разных рецептах
        общее колличество суммируется."""
        final_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]

        file_text = 'Список покупок:\n'
        for item in final_list:
            amount = final_list[item]['amount']
            measurement_unit = final_list[item]['measurement_unit']
            file_text = (f'{file_text}{item}: {amount} {measurement_unit}.\n')

        filename = 'shopping_cart.txt'
        response = HttpResponse(file_text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            filename)
        return response

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """Функция обратабыющая запросы на удаление/добавления
        рецепта в корзину покупок."""
        user = request.user

        if request.method == 'POST':
            if Cart.objects.filter(user=user, recipe__id=pk).exists():
                return Response({
                    'errors': 'Рецепт уже добавлен в корзину'
                }, status=status.HTTP_400_BAD_REQUEST)

            recipe = get_object_or_404(Recipe, pk=pk)
            Cart.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubscriberSerializers(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            obj = Cart.objects.filter(user=user, recipe__id=pk)
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
    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializers
    pagination_class = None
    permission_classes = [AllowAny, ]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None
    permission_classes = [AllowAny, ]


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.ListModelMixin, viewsets.GenericViewSet):

    pass


class FollowViewSet(CreateRetrieveViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return current_user.follower.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        """Функция обрабатывающая запросы на создание/удаление
        подписки на автора."""
        user = request.user
        author = get_object_or_404(User, pk=pk)

        if request.method == 'DELETE':
            if user == author:
                return Response({
                    'errors': 'Вы не можете отписываться от самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response({
                'errors': 'Вы уже отписались'
            }, status=status.HTTP_400_BAD_REQUEST)

        if user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.get_or_create(user=user, author=author)
        serializer = FollowSerializers(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializers(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
