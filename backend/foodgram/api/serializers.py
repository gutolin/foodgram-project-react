from django.contrib.auth import get_user_model
from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from recipe.models import Follow, Ingredient, IngredientAmount, Recipe, Tag

User = get_user_model()


class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializers(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientAmountSerializers(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='name.id')
    name = serializers.ReadOnlyField(source='name.ingredient')
    amount = serializers.ReadOnlyField(source='name.amount')
    measurement_unit = serializers.ReadOnlyField(
        source='name.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'measurement_unit', 'amount']


class UsersSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class RecipeSerializers(serializers.ModelSerializer):
    tags = TagSerializers(read_only=True, many=True)
    ingredients = SerializerMethodField()
    author = UsersSerializer(read_only=True, many=False)
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  'is_favorited',
                  'is_in_shopping_cart'
                  ]

    def get_ingredients(self, recipe: Recipe):
        """Получение ингредиентов связанных с рецептом."""
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingridient__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        """Получение статуса избранного."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Получение статуса в корзине."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()


class FollowSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count']

    def get_is_subscribed(*args):
        """Получение статуса подписки на автора."""
        return True

    def get_recipes(self, obj):
        """Получение рецепта."""
        print(obj)
        print(obj[0])
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeSubscriberSerializers(queryset, many=True).data

    def get_recipes_count(self, obj):
        print(obj)
        """Получение колличества рецептов."""
        return Recipe.objects.filter(author=obj.author).count()


class RecipeSubscriberSerializers(serializers.ModelSerializer):
    """Краткая версия сериализатора рецепта."""
    class Meta:
        model = Recipe
        fields = ['id',
                  'name',
                  'image',
                  'cooking_time',
                  ]


class RecipeCreateSerializers(serializers.ModelSerializer):
    tags = TagSerializers(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  'is_favorited',
                  'is_in_shopping_cart'
                  ]

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_ingredients(self, recipe: Recipe):
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingridient__amount')
        )
        return ingredients

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')

        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Пустое значение ингредиента'})
        ingredient_list = set()

        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id']
                                           )

            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингридиенты должны быть уникальными'
                    )
            ingredient_list.add(ingredient)

            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError(
                    {'ingredients': (
                        'Значение колличества не может быть меньше 0'
                        )
                     })
        data['ingredients'] = ingredients

        return data

    def create_ingredients(self, ingredients, recipe):
        """Создание ингредиента в случае отсутствия нужного в БД."""
        data = []
        for ingredient in ingredients:
            element = IngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
            )
            data.append(element)
        IngredientAmount.objects.bulk_create(data)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


class UserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'password', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                {'Выберите другой username'})
        return data
