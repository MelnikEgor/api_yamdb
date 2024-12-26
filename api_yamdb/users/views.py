import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status, mixins, generics
# from rest_framework.permissions import IsAdminUser, AllowAny
# from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .serializers import UserSerializer, UserMeSerializer, SignUpSerializer, TokenSerialiser
from api.permissions import IsAdminAndIsAuthenticated
from rest_framework.exceptions import MethodNotAllowed 


User = get_user_model()


class UserSignUpView(generics.GenericAPIView):  # viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serailizer = self.get_serializer(data=request.data)
        serailizer.is_valid(raise_exception=True)
        print('*' * 80, serailizer.is_valid(), '*' * 80)
        print('*' * 80, serailizer.validated_data, '*' * 80)
        user, created = User.objects.get_or_create(
            username=serailizer.validated_data['username'],
            defaults={'email': serailizer.validated_data['email']}
        )
        self.send_confirmation_code(user)
        return Response(
            serailizer.validated_data,
            # {
            #     'username': user.username,
            #     'email': user.email
            # },
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
    permission_classes = (AllowAny,)
    serializer_class = TokenSerialiser

    def post(self, request):
        # user = get_object_or_404(
        #     User.objects.all(),
        #     username=request.data.get('username')
        # )
        serailizer = self.get_serializer(data=request.data)
        serailizer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User.objects.all(),
            username=serailizer.validated_data['username']
        )
        if user.confirmation_code == request.data.get('confirmation_code'):
            return Response(
                {
                    'token': str(AccessToken.for_user(user))
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({'error': 'Не верный код подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     user = User.objects.get(username=request.data.get('username'))
        #     if user.confirmation_code == request.data.get('confirmation_code'):
        #         return Response(
        #             {
        #                 'token': str(AccessToken.for_user(user))
        #             },
        #             status=status.HTTP_200_OK
        #         )
        #     else:
        #         return Response({'error': 'Не верный код подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)
        # except User.DoesNotExist:
        #     return Response({'error': 'Нет такого пользователя.'}, status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
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
    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'PUT':
    #         raise MethodNotAllowed('PUT')
    #     return super().dispatch(request, *args, **kwargs)


class UserMeVeiw(APIView):
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
