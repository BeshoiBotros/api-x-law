from django.shortcuts import render
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response

class ClientRegister(APIView):
    permission_classes=[]
    def post(self, request):
        serializer = serializers.ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

