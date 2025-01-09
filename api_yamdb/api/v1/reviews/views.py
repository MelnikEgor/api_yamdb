from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from .base_views import (
    BaseExceptFullUpdataViewSet,
    BaseNoRetrieveAndNoUpdataViewSet
)
from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer
)
from reviews.models import Category, Comment, Genre, Review, Title
from api.v1.permissions import IsAdminOrReadOnly


User = get_user_model()


class CategoryViewSet(BaseNoRetrieveAndNoUpdataViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseNoRetrieveAndNoUpdataViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(BaseExceptFullUpdataViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    # permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        permission_classes = [IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        title = self.get_object()
        serializer = self.get_serializer(title)
        rating = title.reviews.aggregate(Avg('score'))['score__avg']
        data = serializer.data
        data['rating'] = rating
        return Response(data)


class ReviewViewSet(BaseExceptFullUpdataViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        # title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()
        # title_id = self.kwargs.get('title_id')
        # return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        # title_id = self.kwargs.get('title_id')
        title = self.get_title()  # get_object_or_404(Title, id=title_id)
        author = self.request.user
        serializer.save(author=author, title=title)


class CommentViewSet(BaseExceptFullUpdataViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        reviews = title.reviews.all()
        return get_object_or_404(reviews, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        review = self.get_review()  # self.kwargs.get('review_id')
        return review.comments.all()  # Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        # review_id = self.kwargs.get('review_id')
        review = self.get_review()  # get_object_or_404(Review, id=review_id)
        author = self.request.user
        serializer.save(author=author, review=review)
