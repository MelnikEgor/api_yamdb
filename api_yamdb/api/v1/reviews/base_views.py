from rest_framework import mixins, permissions, viewsets
from rest_framework.filters import SearchFilter

from api.v1.mixins import CastomUpdateModelMixin
from api.v1.permissions import IsAdminOrModerOrReadOnly, IsAdminOrReadOnly


class BaseNoRetrieveAndNoUpdataViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class BaseExceptFullUpdataViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    CastomUpdateModelMixin,
    viewsets.GenericViewSet
):
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrModerOrReadOnly]
        return [permission() for permission in permission_classes]
