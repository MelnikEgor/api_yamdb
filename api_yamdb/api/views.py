from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)

from .filters import TitleFilter
from .permissions import IsAdminOrModerOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class BaseModelViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)


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

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)


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
