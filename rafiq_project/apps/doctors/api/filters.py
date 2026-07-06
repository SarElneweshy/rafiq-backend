import django_filters
from rest_framework.exceptions import ValidationError
from apps.doctors.models import Doctor

class DoctorFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="istartswith"
    )
    city = django_filters.CharFilter(
        field_name="city",
        lookup_expr="iexact"
    )
    area = django_filters.CharFilter(
        field_name="area",
        lookup_expr="iexact"
    )
    min_rating = django_filters.NumberFilter(
        method="filter_min_rating"
    )
    def filter_min_rating(self, queryset, name, value):
        if value is None:
            return queryset
        if value < 0 or value > 5:
            raise ValidationError({
                "min_rating": "Rating must be between 0 and 5."
            })
        return queryset.filter(
            rating__gte=value
        )
    class Meta:
        model = Doctor
        fields = [
            "name",
            "city",
            "area",
            "min_rating",
        ]
    