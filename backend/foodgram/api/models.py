from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100, 
                            unique=True,
                            verbose_name='Tag')
    color = models.CharField(max_length=7,
                             unique=True,
                             verbose_name='Цвет')
    slug = models.SlugField(unique=True,
                            verbose_name='slug')

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=10,
                                        verbose_name='Единица измерения')

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='recipes')
    name = models.CharField(max_length=200,
                            verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/', 
                              null=True,
                              verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиент',
        related_name='recipes'
        )
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Тэги',
                                  related_name='recipes')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготоваления'
        )

    def __str__(self) -> str:
        return self.name


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        UniqueConstraint(fields=['user', 'following'], name='unique_follow')

    def __str__(self):
        return f'{self.user} following {self.following}'


class IngredientAmount(models.Model):
    name = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        related_name='ingridient'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe'
    )
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} for {self.recipe}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        UniqueConstraint(fields=['user', 'recipe'],
                         name='unique_cart')
