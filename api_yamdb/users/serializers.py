import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from .models import ROLE
from api_yamdb.settings import DEFAULT_FROM_EMAIL, PATERN_USER


User = get_user_model()


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
        
#         token = super().get_token(user)

#         # Add custom claims
#         token['name'] = user.name
#         # ...

#         return token


class TokenSerialiser(serializers.ModelSerializer):
    username = serializers.RegexField(PATERN_USER, max_length=50)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class SignUpSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    username = serializers.RegexField(PATERN_USER, max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email',)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                # message='У вас уже имеется подписка на данного пользователя.'
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не должно быть 'me'"
            )
        return value

    # def create(self, validated_data):
    #     user = User.objects.create(**validated_data)
    #     self.send_confirmation_code(user)
    #     return user

    # def send_confirmation_code(self, user):
    #     confirmation_code = uuid.uuid5(uuid.NAMESPACE_DNS, user.username)
    #     user.confirmation_code = confirmation_code
    #     user.save()
    #     send_mail(
    #         subject='Код подтверждения',
    #         message=f'Ваш код подтверждения: {confirmation_code}.',
    #         from_email=DEFAULT_FROM_EMAIL,
    #         recipient_list=[user.email],
    #         fail_silently=True,
    #     )
        # user = User.objects.create(
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        # )


class UserSerializer(serializers.ModelSerializer):
    # role = serializers.ChoiceField(choices=ROLE, allow_blank=True)
    username = serializers.RegexField(
        PATERN_USER,
        max_length=50,
        validators=[UniqueValidator(
            queryset=User.objects.all()
                #fields=('username',),
                # message='У вас уже имеется подписка на данного пользователя.'
        )]
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
        # validators = [
        #     UniqueValidator(
        #         queryset=User.objects.all(),
        #         fields=('username',),
        #         # message='У вас уже имеется подписка на данного пользователя.'
        #     )
        # ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Имя пользователя не должно быть 'me'"
            )
        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        if user.role == 'admin':
            user.is_staff = True
            user.save()
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        #     role=validated_data['role'] if validated_data['role'],
        #     is_staff=True if validated_data['role'] == 'admin' else False
        # )
        return user

    # def create(self, validated_data):
    #     print(self.request.data)
    #     # serializer = UserSerializer(data=request.data)
    #     if self.request.data['username'] != 'me':
    #         return User.objects.create(**validated_data)
    #         # return super().create(request)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
