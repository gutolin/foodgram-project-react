from django.contrib import admin

from .models import Follow, Recipe, Tag, Ingredient, IngredientAmount, Cart

admin.site.register(Follow)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Cart)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
