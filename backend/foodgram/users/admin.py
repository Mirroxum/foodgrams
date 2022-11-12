from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import User
from foodgram.conf import EMPTY_VALUE


@register(User)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )

    fields = (
        ('username', 'email',),
        ('first_name', 'last_name', ),
        ('subscribe',),
    )
    fieldsets = []
    search_fields = (
        'username', 'email',
    )
    list_filter = ('username', 'email')
    empty_value_display = EMPTY_VALUE
