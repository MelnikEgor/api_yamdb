from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.constants import (
    CONFIRMATION_CODE_MAX_LENGTH,
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


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        PATERN_USER,
        max_length=USERNAME_MAX_LENGTH
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    # def validate(self, data):
    #     try:
    #         print('*'*60, data.get('username'), '*'*60)
    #         user = User.objects.get(username=data.get('username'))
    #         print('*'*60, user.email, '*'*60)
    #         if user.email != data.get('email'):
    #             raise serializers.ValidationError('Электронная почта указана не верно.')
    #     except User.DoesNotExist:
    #         print('*'*60, data, '*'*60)
    #         return super().validate(data)
    #         # serializer.is_valid(raise_exception=True)
    #         # user = User.objects.create(**serializer.validated_data)
    #     # else:
    #             # return Response(
    #             #     {
    #             #         'error': 'Электронная почта указана не верно.'
    #             #     },
    #             #     status=status.HTTP_400_BAD_REQUEST
    #             # )
    #     return data
    #     # return super().validate(data)

    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f"Имя пользователя не должно быть '{value}'"
            )
        return value


class UserSerializer(serializers.ModelSerializer):
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

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f"Имя пользователя не должно быть '{value}'"
            )
        return value
