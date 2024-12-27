from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import PATERN_USER


User = get_user_model()


class TokenSerialiser(serializers.ModelSerializer):
    username = serializers.RegexField(PATERN_USER, max_length=50)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(PATERN_USER, max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не должно быть 'me'"
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
        if value == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не должно быть 'me'"
            )
        return value


class UserMeSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(PATERN_USER, max_length=50)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не должно быть 'me'"
            )
        return value
