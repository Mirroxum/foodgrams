from django.contrib.admin import register, ModelAdmin

from .models import User
from foodgram.conf import EMPTY_VALUE


@register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )

    fields = (
        ('username', 'email',),
        ('first_name', 'last_name',),
        ('password'),
        ('subscribe',),
    )
    fieldsets = []
    search_fields = (
        'username', 'email',
    )
    list_filter = ('username', 'email')
    empty_value_display = EMPTY_VALUE
