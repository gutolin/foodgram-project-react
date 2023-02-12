from django.contrib import admin

from .models import Follow, Recipe, Tag, Ingredient, IngredientAmount

admin.site.register(Follow)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
