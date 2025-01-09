from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    UserSerializer, SignUpSerializer, TokenSerialiser
)
from .utils import send_confirmation_code
from api.v1.mixins import CastomUpdateModelMixin
from api.v1.permissions import IsAdminAndIsAuthenticated


User = get_user_model()


class UserSignUpView(APIView):
    """Представление регистрации и получения кода подтверждения."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user, _ = User.objects.get_or_create(
        #     username=serializer.validated_data['username'],
        #     defaults={'email': serializer.validated_data['email']}
        # )
        try:
            user = User.objects.get(username=request.data.get('username'))
        except User.DoesNotExist:
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(**serializer.validated_data)
        else:
            if user.email != request.data.get('email'):
                return Response(
                    {
                        'error': 'Электронная почта указана не верно.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        send_confirmation_code(user)
        return Response(
            serializer.initial_data,
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    """Представление получения токена для аутентификации."""

    def post(self, request):
        serializer = TokenSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        if default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code']
        ):
            return Response(
                {
                    'token': str(AccessToken.for_user(user))
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'error': 'Не верный код подтверждения.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    CastomUpdateModelMixin,
    viewsets.GenericViewSet
):
    """Представление администратора для управления пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username']
    permission_classes = (IsAdminAndIsAuthenticated,)

    @action(
        detail=False,
        methods=['GET'],  # , 'PATCH'],
        permission_classes=(IsAuthenticated, ),
        url_path='me'
    )
    def me(self, request):
        # if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
        # if request.method == 'PATCH':
        #     serializer = UserSerializer(
        #         get_object_or_404(User, email=request.user),
        #         data=request.data,
        #         partial=True
        #     )
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save(role=request.user.role)
        #     return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def patch_me(self, request):
        serializer = UserSerializer(
            get_object_or_404(User, email=request.user),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
