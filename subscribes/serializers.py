from rest_framework import serializers
from . import models

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscribe
        fields = '__all__'

class SubscribeContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscribeContract
        fields = '__all__'


class SubscribeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscribeOrder
        fields = '__all__'

