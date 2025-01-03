from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    UserSerializer, SignUpSerializer, TokenSerialiser
)
from .utils import send_confirmation_code
from api.v1.permissions import IsAdminAndIsAuthenticated
from api_yamdb.mixins import CastomUpdateModelMixin


User = get_user_model()


class UserSignUpView(APIView):
    """Представление регистрации и получения кода подтверждения."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        try:
            user = User.objects.get(username=request.data.get('username'))
        except User.DoesNotExist:
            # serializer = SignUpSerializer(data=request.data)
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
            # {
            #     'username': user.username,
            #     'email': user.email
            # },
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    """Представление получения токена для аутентификации."""

    def post(self, request):
        serializer = TokenSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User.objects.all(),
            username=serializer.validated_data['username']
        )
        if user.confirmation_code == request.data.get('confirmation_code'):
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
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated, ),
        url_path='me'
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                get_object_or_404(User.objects.all(), email=request.user),
                data=request.data,
                partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
