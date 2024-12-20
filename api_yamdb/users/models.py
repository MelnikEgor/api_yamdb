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
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=16, choices=ROLE, default='user')

    # class Meta:
    #     verbos_name = 'User'
    #     verbos_name_plural = 'Users'
