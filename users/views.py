from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from XLaw import shortcuts
from . import models

class ClientRegister(APIView):
    permission_classes=[]
    def post(self, request):
        serializer = serializers.ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ClientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            client = shortcuts.object_is_exist(pk, models.Client, exception="Client Not Found")
            serializer = serializers.ClientSerializer(client)
            return Response(serializer.data)
        clients = models.Client.objects.all()
        serializer = serializers.ClientSerializer(clients, many=True)

    def patch(self, request):
        is_client = shortcuts.is_client(request)
        if is_client:
            client = shortcuts.object_is_exist(request.user.pk, models.Client, exception="Client Not Found")
            serializer = serializers.ClientSerializer(instance=client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        return Response({'Error' : 'Only Clients can update their accounts data here'})

class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            user = shortcuts.object_is_exist(pk, models.CustomUser, exception="user Not Found")
            serializer = serializers.ClientSerializer(user)
            return Response(serializer.data)
        