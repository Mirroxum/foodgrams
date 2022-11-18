from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import User
from foodgram.conf import EMPTY_VALUE


@register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Subscribe', {'fields': ('subscribe')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),}),)
    search_fields = (
        'username', 'email',
    )
    list_filter = ('username', 'email')
    empty_value_display = EMPTY_VALUE
