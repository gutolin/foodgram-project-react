from django.contrib import admin

from recipe.models import (Cart, Favorites, Follow, Ingredient,
                           IngredientAmount, Recipe, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientAmount


class RuleRecipe(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    min_num = 1


admin.site.register(Recipe, RuleRecipe)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Cart)
admin.site.register(Favorites)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
