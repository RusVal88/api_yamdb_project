from django_filters import rest_framework

from review.models import Titles


class TitlesFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )
    genre = rest_framework.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains',
    )
    category = rest_framework.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains',
    )

    class Meta:
        model = Titles
        fields = (
            'name',
            'category',
            'genre',
            'year',
        )
