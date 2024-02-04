import django_filters
from . import models

class NewFilters(django_filters.FilterSet):
    class Meta:
        model = models.New
        fields = '__all__'

class CaseFilters(django_filters.FilterSet):
    class Meta:
        model = models.Case
        fields = '__all__'

class CategoryFilters(django_filters.FilterSet):
    class Meta:
        model = models.Category
        fields = '__all__'