from django.db.models import Q
from django_filters import rest_framework as filters
from migration_backend.processes.models import Movie

class MovieFilter(filters.FilterSet):
    genres = filters.CharFilter(method='filter_by_genres')

    class Meta:
        model = Movie
        fields = []

    def filter_by_genres(self, queryset, name, value):
        genre_list = value.split('|')
        query = Q()
        for genre in genre_list:
            query |= Q(genres__icontains=genre)
        return queryset.filter(query)
