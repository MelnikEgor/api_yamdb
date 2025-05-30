from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']
