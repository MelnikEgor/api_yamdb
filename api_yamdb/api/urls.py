from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include([
        path('', include(router.urls)),
        path('titles/<int:title_id>/reviews/',
             ReviewViewSet.as_view({'get': 'list', 'post': 'create'}),
             name='reviews-list'),
        path('titles/<int:title_id>/reviews/<int:pk>/', ReviewViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update',
             'delete': 'destroy'}), name='reviews-detail'),
        path('titles/<int:title_id>/reviews/<int:review_id>/comments/',
             CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
             name='comments-list'),
        path('titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/', CommentViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='comments-detail'),
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')),
    ])),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import UserViewSet, UserMeVeiwSet

router_api_v1 = DefaultRouter()

# Регистрация всех необходимых вьюсетов
router_api_v1.register(r'categories', CategoryViewSet, basename='category')
router_api_v1.register(r'genres', GenreViewSet, basename='genre')
router_api_v1.register(r'titles', TitleViewSet, basename='title')
router_api_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

# router_api_v1.register(
#     'users/me',
#     UserMeVeiwSet,
#     basename='users_me'
# )

urlpatterns = [
    path('v1/users/me/', UserMeVeiwSet.as_view()),
    path('v1/', include(router_api_v1.urls)),
]
