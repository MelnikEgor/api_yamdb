from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   DestroyModelMixin)
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title, TitleGenre, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerializer, CommentSerializer)
from .permissions import IsAdminOrReadOnly, IsAdminOrModerOrReadOnly

from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, viewsets

from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed


User = get_user_model()


class BaseModelViewSet(CreateModelMixin, ListModelMixin,
                       DestroyModelMixin, GenericViewSet):
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # filter_backends = (SearchFilter,)
    # search_fields = ('name',)
    # permission_classes = [IsAdminOrReadOnly]
    # lookup_field = 'slug'


class GenreViewSet(BaseModelViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # filter_backends = (SearchFilter,)
    # search_fields = ('name',)
    # permission_classes = (IsAdminOrReadOnly,)
    # lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.prefetch_related('genre', 'category').all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        genres_data = self.request.data.get('genre')
        category_data = self.request.data.get('category')

        # Проверка существования категории
        try:
            category = Category.objects.get(slug=category_data)
        except Category.DoesNotExist:
            raise ValidationError(
                {'category': 'Указанная категория не существует.'})

        # Проверка существования жанров
        genres = []
        for genre_slug in genres_data:
            try:
                genre = Genre.objects.get(slug=genre_slug)
                genres.append(genre)
            except Genre.DoesNotExist:
                raise ValidationError(
                    {'genre': f'Жанр {genre_slug} не существует.'})

        title = serializer.save(category=category)

        # Сохранение жанров через промежуточную таблицу
        for genre in genres:
            TitleGenre.objects.create(title=title, genre=genre)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')

        instance = self.get_object()
        serializer = self.get_serializer(
            data=request.data, partial=False)
        
        print('*'*60, serializer.is_valid(), '*'*60)
        # print('*'*60, serializer.data, '*'*60)
        print('*'*60, serializer, '*'*60)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrModerOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        author = self.request.user

        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Вы уже оставили отзыв на это произведение.')

        serializer.save(author=author, title=title)

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrModerOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        author = self.request.user

        serializer.save(author=author, review=review)
