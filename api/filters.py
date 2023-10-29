import django_filters
from catalogue.models import Book
from django.db.models import Q


class BookFilter(django_filters.FilterSet):
    # Custom filters
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    ISBN = django_filters.CharFilter(field_name="ISBN", lookup_expr="icontains")

    author_name = django_filters.CharFilter(method="filter_by_author_full_name")

    class Meta:
        model = Book
        fields = []

    # This function will perform the 'author' filtering.

    def filter_by_author_full_name(self, queryset, name, value):
        # Splitting by spaces, assuming that first and last names are separated by spaces
        names = value.split()

        # We create queries for each word, assuming it could be either first or last name.
        queries = [
            Q(author__first_name__icontains=name) | Q(author__last_name__icontains=name)
            for name in names
        ]

        # Start with a base query which includes the entire queryset
        query = Q(pk__in=queryset)

        # 'AND' the name queries together
        for q in queries:
            query &= q

        return queryset.filter(query)
