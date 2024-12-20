from django.contrib.auth import get_user_model
from django.shortcuts import render, get_list_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer


User = get_user_model()


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username']

    def create(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if request.data['username'] != 'me':
            return super().create(request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['get', 'patch'])
    # def me(self, request):
    #     user = get_list_or_404(User.objects.all(), username=request.user)
    #     serializer = UserSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeVeiwSet(
    # viewsets.GenericViewSet,
    # mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin
    APIView
):
    def get_user(request):
        return get_list_or_404(User.objects.all(), username=request.user.username)

    def get(self, request):
        user = get_list_or_404(User.objects.all(), username=request.user)  # self.get_user()
    # serializer_class = UserSerializer
        print(user)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def patch(self, request):
        user = get_list_or_404(User.objects.all(), username=request.user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
