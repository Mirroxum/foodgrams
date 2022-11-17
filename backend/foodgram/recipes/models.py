from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import is_hex_color
from foodgram.conf import MAX_LEN_RECIPES_CHARFIELD, MAX_LEN_RECIPES_TEXTFIELD

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LEN_RECIPES_CHARFIELD,
        unique=True,
    )
    color = models.CharField(
        validators=[is_hex_color],
        verbose_name='Цветовой HEX-код',
        max_length=7,
        blank=True,
        null=True,
        default='#FFFFFF'
    )
    slug = models.SlugField(
        verbose_name='Slug тега',
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} - {self.slug}'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=MAX_LEN_RECIPES_CHARFIELD,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=MAX_LEN_RECIPES_CHARFIELD
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name', )
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit', ),
                name='unique_for_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=MAX_LEN_RECIPES_CHARFIELD,
        unique=True
    )
    image = models.ImageField(
        verbose_name='Изображение для рецепта',
        upload_to='recipes/images/',
    )
    favorite = models.ManyToManyField(
        User,
        verbose_name='Избранные рецепты',
        related_name='favorites'
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=MAX_LEN_RECIPES_TEXTFIELD
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='+'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=(
            MinValueValidator(
                1, 'Нужно указать количество.'
            ),
            MaxValueValidator(
                10000, 'Слишком большое количество'
            ),
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author', ),
                name='unique_for_author'
            ),
        )

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Связанный рецепт',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Связанный ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(
                1, 'Нужно указать количество.'
            ),
            MaxValueValidator(
                10000, 'Слишком большое количество'
            ),
        )
    )

    class Meta:
        verbose_name = 'Связаный ингредиент'
        verbose_name_plural = 'Связаные ингредиенты'

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}\
{self.ingredient.measurement_unit}'


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
        related_name='+',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique cart user')
        ]
