from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from XLaw import shortcuts
from . import models
from django.core.mail import send_mail
import jwt
from XLaw import settings

class CustomUserEmail(APIView):
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
            return Response({'message' : 'We are sending email confermation right now.'})
        else:
            return Response(serializer.errors)

