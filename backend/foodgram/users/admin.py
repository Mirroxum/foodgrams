from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .forms import CustUserChangeForm, CustUserCreationForm
from .models import User
from foodgram.conf import EMPTY_VALUE


@register(User)
class UserAdmin(UserAdmin):
    add_form = CustUserCreationForm
    form = CustUserChangeForm
    model = User
    list_display = (
        'email', 'username', 'first_name', 'last_name',
    )
    list_filter = (
        'email', 'username',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'username', 'first_name', 'last_name', 'password',
            'subscribe',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'password1',
                'password2', 'subscribe',
            )
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    ordering = ('email', 'username',)
    list_filter = ('username', 'email')
    empty_value_display = EMPTY_VALUE
