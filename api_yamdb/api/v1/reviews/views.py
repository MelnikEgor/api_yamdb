from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

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
    # TitleSerializer
    TitleReadSerializer,
    TitleWriteSerializer
)
from api.v1.mixins import CastomUpdateModelMixin
from api.v1.permissions import IsAdminOrReadOnly
from reviews.models import Category, Genre, Title


User = get_user_model()


class CategoryViewSet(BaseNoRetrieveAndNoUpdataViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseNoRetrieveAndNoUpdataViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


# class TitleViewSet(BaseExceptFullUpdataViewSet):
#     queryset = Title.objects.all()
#     serializer_class = TitleSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = TitleFilter
#     # permission_classes = [IsAdminOrReadOnly]

#     def get_permissions(self):
#         permission_classes = [IsAdminOrReadOnly]
#         return [permission() for permission in permission_classes]

#     def retrieve(self, request, *args, **kwargs):
#         title = self.get_object()
#         serializer = self.get_serializer(title)
#         rating = title.reviews.aggregate(Avg('score'))['score__avg']
#         data = serializer.data
#         data['rating'] = rating
#         return Response(data)


# class TitleViewSet(BaseExceptFullUpdataViewSet):
#     queryset = Title.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = TitleFilter

#     def get_serializer_class(self):
#         if self.action in ['list', 'retrieve']:
#             return TitleReadSerializer
#         return TitleWriteSerializer

#     def get_permissions(self):
#         permission_classes = [IsAdminOrReadOnly]
#         return [permission() for permission in permission_classes]

#     def retrieve(self, request, *args, **kwargs):
#         title = self.get_object()
#         serializer = self.get_serializer(title)
#         rating = title.reviews.aggregate(Avg('score'))['score__avg']
#         data = serializer.data
#         data['rating'] = round(rating, 2) if rating is not None else None
#         return Response(data)


class TitleViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    CastomUpdateModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        ).order_by('name')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer

    # def get_permissions(self):
    #     permission_classes = [IsAdminOrReadOnly]
    #     return [permission() for permission in permission_classes]


class ReviewViewSet(BaseExceptFullUpdataViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        author = self.request.user
        serializer.save(author=author, title=title)


class CommentViewSet(BaseExceptFullUpdataViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        reviews = title.reviews.all()
        return get_object_or_404(reviews, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        author = self.request.user
        serializer.save(author=author, review=review)
