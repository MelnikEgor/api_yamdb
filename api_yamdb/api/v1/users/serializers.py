from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .mixins import UserameNotMeMixin
from api_yamdb.constants import (
    CONFIRMATION_CODE_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    PATERN_USER,
    USERNAME_MAX_LENGTH
)


User = get_user_model()


class TokenSerialiser(serializers.Serializer):
    username = serializers.RegexField(
        PATERN_USER,
        max_length=USERNAME_MAX_LENGTH
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH,
        error_messages={
            'blank': 'Код подтверждения не может быть пустым.',
        }
    )


class SignUpSerializer(serializers.ModelSerializer, UserameNotMeMixin):
    username = serializers.RegexField(
        PATERN_USER,
        max_length=USERNAME_MAX_LENGTH,
    )
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        email = data.get('email')
        try:
            user = User.objects.get(username=data.get('username'))
            if user.email != email:
                raise serializers.ValidationError(
                    {
                        'email': 'Электронная почта указана не верно.'
                        'Введите правильный адрес электронной почты.'
                    }
                )
        except User.DoesNotExist:
            if User.objects.filter(email=email):
                raise serializers.ValidationError(
                    {
                        'email': 'Данный адрес электронной '
                        'почты уже существует.'
                    }
                )
        return data


class UserSerializer(serializers.ModelSerializer, UserameNotMeMixin):
    username = serializers.RegexField(
        PATERN_USER,
        max_length=USERNAME_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
