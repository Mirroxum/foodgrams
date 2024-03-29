from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram import conf
from .validators import (MinLenValidator, OneOfTwoValidator,
                         UsernameNotMeValidator)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=conf.MAX_LEN_EMAIL_FIELD,
        unique=True,
        help_text=conf.USERS_HELP_EMAIL
    )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=conf.MAX_LEN_USERS_CHARFIELD,
        unique=True,
        help_text=(conf.USERS_HELP_UNAME),
        validators=(
            MinLenValidator(),
            OneOfTwoValidator(),
            UsernameNotMeValidator(),
        ),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=conf.MAX_LEN_USERS_CHARFIELD,
        help_text=conf.USERS_HELP_FNAME,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=conf.MAX_LEN_USERS_CHARFIELD,
        help_text=conf.USERS_HELP_FNAME
    )
    subscribe = models.ManyToManyField(
        blank=True,
        to='self',
        verbose_name='Подписка',
        symmetrical=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}: {self.email}'
