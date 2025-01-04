from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet
)
from users.views import TokenView, UserSignUpView, UserViewSet


router_api_v1 = DefaultRouter()

router_api_v1.register(r'users', UserViewSet, basename='users')
router_api_v1.register(r'categories', CategoryViewSet, basename='category')
router_api_v1.register(r'genres', GenreViewSet, basename='genre')
router_api_v1.register(r'titles', TitleViewSet, basename='title')
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/signup/', UserSignUpView.as_view()),
    path('auth/token/', TokenView.as_view()),
    path('', include(router_api_v1.urls)),
]
