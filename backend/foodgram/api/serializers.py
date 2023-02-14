from api.models import Recipe, Ingredient, IngredientAmount, Tag, Follow
from rest_framework import serializers

from user.serializers import UserSerializer

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
    ingredients = IngredientAmountSerializers(
        source='ingredientamount_set',
        many=True,
        read_only=True,
    )
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
