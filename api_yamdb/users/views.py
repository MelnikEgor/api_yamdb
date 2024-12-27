import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    UserSerializer, UserMeSerializer, SignUpSerializer, TokenSerialiser
)
from api.permissions import IsAdminAndIsAuthenticated
from api_yamdb.settings import DEFAULT_FROM_EMAIL


User = get_user_model()


class UserSignUpView(generics.GenericAPIView):
    """Представление регистрации и получения кода подтверждения."""

    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
        except User.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
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
        self.send_confirmation_code(user)
        return Response(
            {
                'username': user.username,
                'email': user.email
            },
            status=status.HTTP_200_OK
        )

    def send_confirmation_code(self, user):
        confirmation_code = uuid.uuid5(uuid.NAMESPACE_DNS, user.username)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}.',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )


class TokenView(generics.GenericAPIView):
    """Представление получения токена для аутентификации."""

    serializer_class = TokenSerialiser

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
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


class UserViewSet(viewsets.ModelViewSet):
    """Представление вдминистратора для управления пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username']
    permission_classes = (IsAdminAndIsAuthenticated,)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)


class UserMeVeiw(APIView):
    """Представление получения и изменение информации пользователем о себе."""

    permission_classes = (IsAuthenticated, )
    serializer_class = UserMeSerializer

    def get_user(self, request):
        return get_object_or_404(User.objects.all(), username=request.user)

    def get(self, request):
        serializer = UserMeSerializer(self.get_user(request))
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserMeSerializer(
            self.get_user(request),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
