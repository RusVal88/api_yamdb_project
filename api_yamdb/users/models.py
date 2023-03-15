from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_me


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
    username = models.CharField(
        verbose_name='Логин пользователя',
        help_text='Укажите логин',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator(), validate_me],
        error_messages={
            'unique': ('Логин должен быть уникальным!'),
        },
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Укажите имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        help_text='Укажите фамилию',
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        verbose_name='Статус пользователя',
        max_length=50,
        choices=ROLES,
        default=USER,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Укажите адрес электронной почты',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Добавьте биографию',
        null=True,
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
