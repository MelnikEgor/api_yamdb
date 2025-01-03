from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        'Электронная почта',
        unique=True
    )
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', 'email')

    # def __str__(self):
    #     return f'{self.username}'

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     username = cleaned_data.get('username')
    #     if not (email and username):
    #         self.add_error('email', 'Поле не может быть пустым.')
    #         self.add_error('username', 'Поле не может быть пустым.')

    #     return

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username.lower() == 'me':
            raise ValidationError(
                f"Имя пользователя не должно быть '{username}'"
            )
        return username
