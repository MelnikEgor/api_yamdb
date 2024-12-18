from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()

# Регистрация всех необходимых вьюсетов
router.register(r'v1/categories', CategoryViewSet, basename='category')
router.register(r'v1/genres', GenreViewSet, basename='genre')
router.register(r'v1/titles', TitleViewSet, basename='title')

urlpatterns = [
    path('', include(router.urls)),
]