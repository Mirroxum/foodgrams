from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram import conf


class MyUser(AbstractUser):
    ROLES_CHOICES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
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
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=conf.MAX_LEN_USERS_CHARFIELD,
        help_text=conf.USERS_HELP_FNAME
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=conf.MAX_LEN_USERS_CHARFIELD,
        help_text=conf.USERS_HELP_FNAME
    )
    subscribe = models.ManyToManyField(
        to='self',
        verbose_name='Подписка',
        related_name='subscribers',
        symmetrical=False
    )
    role = models.CharField(
        choices=ROLES_CHOICES,
        default='user',
        verbose_name='Роль',
        max_length=14
    )
    access_code = models.CharField(
        max_length=8, default=None, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return f'{self.username}: {self.email}'
