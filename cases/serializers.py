from rest_framework import serializers
from . import models
from users.serializers import CustomUserSerializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.New
        fields = ['title', 'category', 'subject', 'user']

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Case
        fields = ['title', 'category', 'subject', 'user']