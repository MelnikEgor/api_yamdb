from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)


class MyUser(AbstractUser):
    """Кастомная модель пользователя."""

    password = models.CharField('Пароль', max_length=128, blank=True)
    email = models.EmailField('Электронная почта', unique=True)
    username = models.CharField(
        'Имя пользователя',
        max_length=128,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=16,
        choices=ROLE,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        null=True
    )
