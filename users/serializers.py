# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from . import models
from XLaw.shortcuts import emailAlreadyExist


class CustomUserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    as_lawyer = serializers.BooleanField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        email = data.get('email')  # Using get to avoid KeyError
        
        if emailAlreadyExist(email):
            raise serializers.ValidationError({'email': 'Email already exists'})
        
        return data

    
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(read_only=True)
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
        
        if emailAlreadyExist(email):
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        return data

class ClientSerializer(CustomUserSerializer):
    class Meta:
        model = models.Client
        fields = CustomUserSerializer.Meta.fields

class LawyerSerializer(CustomUserSerializer):
    class Meta:
        model = models.Lawyer
        fields = CustomUserSerializer.Meta.fields