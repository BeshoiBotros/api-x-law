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
from django.contrib.auth.models import Group
import uuid

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
            confirmation_token = jwt.encode({'email' : validate_data.get('email'), 'uuid': str(uuid.uuid4())}, settings.SECRET_KEY, algorithm='HS256')
            url_confirmation = f'http://127.0.0.1:8000/users/{for_who}/confirm-email/{confirmation_token}/' # we should replace that URL to the frontend url
            send_mail(
                'Confirm your email for complate the registration',
                f'click the following link to complate registration: {url_confirmation}',
                'XLaw123@gmail.com',
                [validate_data.get('email')],
                fail_silently=False,
            )
            return Response({'message' : 'We are sending email confermation right now.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ClientRegistration(APIView):
    def post(self, request, token):
        paylod = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_email = paylod['email']
        serializer_data = {**request.data}
        serializer = serializers.ClientSerializer(data=serializer_data)
        verify_token_serializer = serializers.VerifyToken(data={'token': token})
        if verify_token_serializer.is_valid():
            verify_token_serializer.save()
        else:
            return Response(verify_token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.validated_data['email'] = user_email
            client_instance = serializer.save()
            client_instance.email = user_email
            client_group, created = Group.objects.get_or_create(name='Client')
            client_instance.groups.add(client_group)
            return Response({'message' : 'successfully registration'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LawyerRegistration(APIView):
    def post(self, request, token):
        try:
            is_assestant = request.data.get('is_assestant', None)
        except:
            is_assestant = False
        paylod = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_email = paylod['email']
        serializer_data = request.data.copy()
        serializer_data['email'] = user_email
        serializer = serializers.LawyerSerializer(data=serializer_data)
        verify_token_serializer = serializers.VerifyToken(data={'token': token})
        if verify_token_serializer.is_valid():
            verify_token_serializer.save()
        else:
            return Response(verify_token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            client_instance = serializer.save()
            if not is_assestant:
                client_group, created = Group.objects.get_or_create(name='Lawyer')
            else:
                client_group, created = Group.objects.get_or_create(name='Lawyer Assestant')
            client_instance.groups.add(client_group)
            return Response({'message' : 'successfully registration'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            instance = shortcuts.object_is_exist(pk=pk, model=models.CustomUser, exception="user does not exist")
            serializer = serializers.CustomUserSerializer(instance)
            return Response(serializer.data)
        queryset = models.CustomUser.objects.filter(is_staff=False)
        serializer = serializers.CustomUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = serializers.CustomUserSerializer(instance=user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request):
        user = request.user
        user.is_active = False
        return Response({"message":"user has been deleted successfully"}, status=status.HTTP_200_OK)

class LawyerProfileView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, pk=None):
        if pk:
            instance = shortcuts.object_is_exist(pk=pk, model=models.LawyerProfile, exception="that profile not found")
            serializer = serializers.LawyerProfileSerializer(instance)
            return Response(serializer.data)
        queryset = models.LawyerProfile.objects.all()
        serializer = serializers.LawyerProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def patch(self, request):
        is_lawyer = request.user.is_lawyer
        print(is_lawyer)
        if is_lawyer:
            lawyer_profile_instance = models.LawyerProfile.objects.get(lawyer = request.user.pk)
            lawyer_profile_serializer = serializers.LawyerProfileSerializer(instance=lawyer_profile_instance, data=request.data)
            if lawyer_profile_serializer.is_valid():
                lawyer_profile_serializer.save()
                return Response(lawyer_profile_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(lawyer_profile_serializer.errors)
        return Response({"message" : "you are not lawyer, which mean that can not have profile."})

