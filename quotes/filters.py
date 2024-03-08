import django_filters
from django.db.models import Q
from django_filters import rest_framework

from quotes.models import Quote


class QuotesListFilter(rest_framework.FilterSet):
    tags = django_filters.CharFilter(method='filter_by_tags')
    term = django_filters.CharFilter(
        field_name="content",
        lookup_expr="contains",
    )

    class Meta:
        model = Quote
        fields = (
            "author",
            "tags",
            "term",
        )

    def filter_by_tags(self, queryset, name, value):
        tags = value.split(',')
        query = Q()
        for tag in tags:
            query &= Q(tags__contains=tag)
        return queryset.filter(query)
