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
