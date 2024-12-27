from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet
)
from users.views import TokenView, UserMeVeiw, UserSignUpView, UserViewSet


router_api_v1 = DefaultRouter()

router_api_v1.register(r'users', UserViewSet, basename='users')
router_api_v1.register(r'categories', CategoryViewSet, basename='category')
router_api_v1.register(r'genres', GenreViewSet, basename='genre')
router_api_v1.register(r'titles', TitleViewSet, basename='title')
router_api_v1.register(
    r'posts/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('v1/auth/signup/', UserSignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/users/me/', UserMeVeiw.as_view()),
    path('v1/', include([
        path('', include(router_api_v1.urls)),
        # path(
        #     'titles/<int:title_id>/reviews/',
        #     ReviewViewSet.as_view({'get': 'list', 'post': 'create'}),
        #     name='reviews-list'
        # ),
        # path(
        #     'titles/<int:title_id>/reviews/<int:pk>/',
        #     ReviewViewSet.as_view(
        #         {
        #             'get': 'retrieve',
        #             'patch': 'partial_update',
        #             'delete': 'destroy'
        #         }
        #     ),
        #     name='reviews-detail'
        # ),
        path(
            'titles/<int:title_id>/reviews/<int:review_id>/comments/',
            CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
            name='comments-list'
        ),
        path(
            'titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/',
            CommentViewSet.as_view(
                {
                    'get': 'retrieve',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                }
            ),
            name='comments-detail'
        ),
    ])),
]
