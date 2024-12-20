from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerializer, CommentSerializer)


class BaseModelViewSet(viewsets.ModelViewSet):
    filter_backends = []
    search_fields = []
    permission_classes = []

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class GenreViewSet(BaseModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class TitleViewSet(BaseModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']


class ReviewViewSet(BaseModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = Title.objects.get(id=title_id)
        serializer.save(author=self.request.user, title_id=title)
        # self.recalculate_rating(title)
        author = self.request.user
        # if Review.objects.filter(title_id=title_id, author=author).exists():
        #     raise ValidationError('Вы уже оставили отзыв на это произведение.')

    def perform_update(self, serializer):
        instance = serializer.save()
        # instance.title.recalculate_rating()

    def perform_destroy(self, instance):
        # title = instance.title
        instance.delete()
        # title.recalculate_rating()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
