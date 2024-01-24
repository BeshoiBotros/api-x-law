# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()

def emailAlreadyExist(email):
    return User.objects.filter(email=email).exists()


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_client = serializers.BooleanField(read_only=True)
    is_lawyer = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = models.CustomUser  
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_client', 'is_lawyer']

    def validate(self, attrs):
        data = super().validate(attrs)
        email = data.get('email')  # Using get to avoid KeyError
        
        if email and emailAlreadyExist(email):
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        return data
