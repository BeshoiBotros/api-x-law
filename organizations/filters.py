import django_filters
from . import models

class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = models.Organization
        fields = '__all__'

