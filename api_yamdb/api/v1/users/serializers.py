from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.constants import PATERN_USER


User = get_user_model()


class TokenSerialiser(serializers.Serializer):
    username = serializers.RegexField(PATERN_USER, max_length=150)
    confirmation_code = serializers.CharField(max_length=255)

    def validate_confirmation_code(self, value):
        if not value:
            raise serializers.ValidationError(
                'Код подтверждения не может быть пустым.'
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(PATERN_USER, max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f"Имя пользователя не должно быть '{value}'"
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        PATERN_USER,
        max_length=50,
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

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f"Имя пользователя не должно быть '{value}'"
            )
        return value
