from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


class CastomUpdateModelMixin:
    """Миксин для обновления данных без PUT метода."""

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if not partial:
            raise MethodNotAllowed('PUT')
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
