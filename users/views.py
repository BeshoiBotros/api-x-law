from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from XLaw import shortcuts
from . import models
from django.core.mail import send_mail
import jwt
from XLaw import settings
from rest_framework import status

class CustomUserEmail(APIView): # for making URLs to confirm emails
    def post(self, request):
        serializer = serializers.CustomUserEmailSerializer(data=request.data)
        for_who = None
        if serializer.is_valid():
            validate_data = serializer.validated_data
            if validate_data.get('as_lawyer'):
                for_who = 'lawyer'
            else:
                for_who = 'client'
            confirmation_token = jwt.encode({'email' : validate_data.get('email')}, settings.SECRET_KEY, algorithm='HS256')
            url_confirmation = f'https://127.0.0.1:8000/users/{for_who}/confirm-email/{confirmation_token}/'
            send_mail(
                'Confirm your email for complate the registration',
                f'click the following link to complate registration: {url_confirmation}',
                'XLaw123@gmail.com',
                validate_data.get('email'),
                fail_silently=False,
            )
            return Response({'message' : 'We are sending email confermation right now.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ClientRegistration(APIView):
    def post(self, request, token):
        paylod = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_email = paylod['email']
        serializer_data = request.data.copy()
        serializer_data['email'] = user_email
        serializer = serializers.ClientSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'successfully registration'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LawyerRegistration(APIView):
    def post(self, request, token):
        paylod = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_email = paylod['email']
        serializer_data = request.data.copy()
        serializer_data['email'] = user_email
        serializer = serializers.LawyerSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'successfully registration'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
