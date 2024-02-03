import django_filters
from . import models

class SubscribeFilter(django_filters.FilterSet):
    class Meta:
        model = models.Subscribe
        fields = '__all__'

