from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.reviews.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet
)
from api.v1.users.views import TokenView, UserSignUpView, UserViewSet


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
