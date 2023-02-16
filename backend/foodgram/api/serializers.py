from api.models import Follow, Ingredient, IngredientAmount, Recipe, Tag
from django.contrib.auth import get_user_model
from django.db.models import F, QuerySet
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
from user.serializers import UserSerializer

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
    name = serializers.ReadOnlyField(source='name.name')
    measurement_unit = serializers.ReadOnlyField(
        source='name.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializers(serializers.ModelSerializer):
    tags = TagSerializers(read_only=True, many=True)
    ingredients = SerializerMethodField()
    author = UserSerializer(read_only=True, many=False)
    is_favorited = True
    is_in_shopping_cart = True

    class Meta:
        model = Recipe
        fields = ['id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time'
                  ]

    def get_ingredients(self, recipe: Recipe):
        """Получает список ингридиентов для рецепта.
        Args:
            recipe (Recipe): Запрошенный рецепт.
        Returns:
            QuerySet[dict]: Список ингридиентов в рецепте.
        """
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingridient__amount')
        )
        return ingredients


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
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeSerializers(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
