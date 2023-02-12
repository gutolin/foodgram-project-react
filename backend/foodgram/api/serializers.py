from django.contrib.auth import get_user_model
from api.models import Recipe, Ingredient, IngredientAmount, Tag, Follow
from rest_framework import serializers

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

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit')


class CustomUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  ]


class RecipeSerializers(serializers.ModelSerializer):
    tags = TagSerializers(read_only=True, many=True)
    ingredients = IngredientAmountSerializers(read_only=True, many=True)
    author = CustomUserSerializers(read_only=True, many=False)

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
