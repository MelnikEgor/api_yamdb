from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)


class MyUser(AbstractUser):
    password = models.CharField('password', max_length=128, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField('Имя пользователя', max_length=128, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=16, choices=ROLE, default='user')
    confirmation_code = models.CharField('Код подтверждения', max_length=255, null=True)

    # class Meta:
    #     verbos_name = 'User'
    #     verbos_name_plural = 'Users'
