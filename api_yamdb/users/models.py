from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        USER = 'user'

    username = models.CharField(
        verbose_name='Логин пользователя',
        help_text='Укажите логин',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username, ]
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
        choices=Role.choices,
        default=Role.USER,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Укажите адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Добавьте биографию',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user',
            )
        ]

    def __str__(self):
        return self.username
