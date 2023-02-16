from django.contrib import admin

from .models import Cart, Follow, Ingredient, IngredientAmount, Recipe, Tag, Favorites

admin.site.register(Follow)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Cart)
admin.site.register(Favorites)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
