from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Tag(models.Model):
    """Модель тэгов используется для добавления тегов к рецептом
    с последующей фильтрацией по ним в запросе.
    Color - цвет тэга в HEX."""
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
    """Модель ингредиентов, пользователь выбирает ингредиенты
    для рецепта из этой модели.
    measurement_unit - единица измерения (г/мл/кг...)."""
    name = models.CharField(max_length=100,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=10,
                                        verbose_name='Единица измерения')

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецептов, основная модель проекта.
    author - привязка к модели пользователя
    ingredients - привязка к модели ингредиент
    tags - привязка к модели тэгов
    cooking_time - время готовки (в минутах)."""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='recipes')
    name = models.CharField(max_length=200,
                            verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/',
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
        validators=[MinValueValidator(1), MaxValueValidator(1440)],
        verbose_name='Время приготоваления'
        )

    def __str__(self) -> str:
        return self.name


class Follow(models.Model):
    """Модель подписок. Создает уникальную запись в бд пользователь-автор."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        UniqueConstraint(fields=['user', 'author'], name='unique_follow')

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class Favorites(models.Model):
    """Модель избранного. Создает уникальную запись в
    бд пользователь-рецепт."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранное',
    )

    class Meta:
        verbose_name = 'Избранное'
        UniqueConstraint(fields=['user', 'recipe'], name='unique_favorites')

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'


class IngredientAmount(models.Model):
    """Модель привязки колличеста ингредиентов к рецепту
    ingredient - привязка к ингредиентам
    recipe - привязка к рецепту
    amount - количество ингредиентов"""
    ingredient = models.ForeignKey(
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
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )

    def __str__(self):
        return f'{self.ingredient} for {self.recipe}'


class Cart(models.Model):
    """Модель корзины, создает уникальную запись в бд пользователь-рецепт"""
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
