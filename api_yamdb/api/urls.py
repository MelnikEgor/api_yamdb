from django.urls import include, path
# from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserMeVeiwSet

router_api_v1 = DefaultRouter()
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
