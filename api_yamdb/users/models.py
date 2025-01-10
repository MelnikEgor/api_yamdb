from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

from api_yamdb.constants import (
    ROLE_ADMIN,
    ROLE_MAX_LENGTH,
    ROLE_MODERATOR,
    ROLE_USER,
    USERNAME_MAX_LENGTH
)


ROLE = (
    (ROLE_USER, 'Пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Админ')
)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        'Электронная почта',
        unique=True,
        error_messages={
            'unique': (
                'Пользователь с такой электронной почтой уже существует.'
            ),
            'blank': 'Адрес электронной почты обязателен.'
        },
    )
    username = models.CharField(
        'Имя пользователя',
        unique=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE,
        default=ROLE_USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', 'email')

    def clean(self):
        super().clean()
        username = self.username
        if username.lower() == 'me':
            raise ValidationError(
                f"Имя пользователя не должно быть '{username}'"
            )

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN or self.is_staff

    @property
    def is_moder(self):
        return self.role == ROLE_MODERATOR
