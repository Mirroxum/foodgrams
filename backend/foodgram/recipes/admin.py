from django.contrib.admin import (ModelAdmin, TabularInline,
                                  register, site)
from django.utils.html import format_html

from .models import Ingredient, Recipe, Tag, AmountIngredient
from foodgram.conf import EMPTY_VALUE

site.site_header = 'Администрирование Foodgram'


class IngredientInline(TabularInline):
    model = AmountIngredient
    extra = 3


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
        'id', 'name', 'author', 'is_favorited'
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
        'name', 'author__username', 'tags'
    )
    inlines = [IngredientInline, ]
    save_on_top = True
    empty_value_display = EMPTY_VALUE

    def is_favorited(self, obj):
        return obj.favorite.count()


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        'name', 'color', 'colored', 'slug',
    )
    search_fields = (
        'name', 'color'
    )
    save_on_top = True
    empty_value_display = EMPTY_VALUE

    def colored(self, obj):
        return format_html(
            f'<span style="background: {obj.color};'
            f'color: {obj.color}";>___________</span>'
        )
    colored.short_description = 'Цвет'


site.register(AmountIngredient)
