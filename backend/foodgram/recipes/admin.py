from django.contrib.admin import ModelAdmin, TabularInline, register, site

from .models import AmountIngredient, Ingredient, Recipe, Tag
from foodgram.conf import EMPTY_VALUE

site.site_header = 'Администрирование Foodgram'


class IngredientInline(TabularInline):
    model = AmountIngredient
    extra = 3


@register(AmountIngredient)
class LinksAdmin(ModelAdmin):
    pass


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = (
        'name', 'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )
    save_on_top = True
    empty_value_display = EMPTY_VALUE


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'name',
    )
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    raw_id_fields = ('author', )
    search_fields = (
        'name', 'author',
    )
    list_filter = (
        'name', 'author__username',
    )
    inlines = (IngredientInline,)
    save_on_top = True
    empty_value_display = EMPTY_VALUE


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        'name', 'color', 'slug',
    )
    search_fields = (
        'name', 'color'
    )
    save_on_top = True
    empty_value_display = EMPTY_VALUE
