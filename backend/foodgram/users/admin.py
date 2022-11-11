from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import MyUser
from foodgram.conf import EMPTY_VALUE


@register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'role',
    )

    fields = (
        ('username', 'email',),
        ('first_name', 'last_name', ),
        ('role',),
        ('subscribe',),
    )
    fieldsets = []
    search_fields = (
        'username', 'email',
    )
    list_filter = ('role', 'username', 'email')
    empty_value_display = EMPTY_VALUE
