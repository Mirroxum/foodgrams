from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User
from foodgram.conf import EMPTY_VALUE


@register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'is_blocked',
        'is_superuser',
    )
    list_filter = (
        'email', 'username', 'is_blocked', 'is_superuser',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'username', 'first_name', 'last_name', 'password',
        )}),
        ('Permissions', {'fields': ('is_blocked', 'is_superuser',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'password1',
                'password2', 'is_blocked', 'is_superuser',
            )
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    ordering = ('id', 'email', 'username',)
    list_filter = ('username', 'email')
    empty_value_display = EMPTY_VALUE
