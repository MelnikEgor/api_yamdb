from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from .models import ROLE

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
    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=('username', 'email'),
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
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE)

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

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        #if user.role:
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
