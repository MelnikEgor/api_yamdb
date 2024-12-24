from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet)
from users.views import UserViewSet, UserMeVeiw, UserSignUpView, TokenView


router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/auth/signup/', UserSignUpView.as_view()),  # {'post': 'create'})),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/users/me/', UserMeVeiw.as_view()),
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
        # path('auth/', include('djoser.urls')),
        # path('auth/', include('djoser.urls.jwt')),
    ])),
]



