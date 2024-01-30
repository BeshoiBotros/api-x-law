from django.shortcuts import render
from . import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import models
from XLaw import shortcuts
from rest_framework.response import Response

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            subscribe_instance = shortcuts.object_is_exist(pk, models.Subscribe, "subscribe not found")
            subscribe_serializer = serializers.SubscribeSerializer(subscribe_instance)
            return Response(subscribe_serializer.data)
        subscribe_queryset = models.Subscribe.objects.all()
        subscribe_serializer = serializers.SubscribeSerializer(subscribe_queryset, many=True)
        return Response(subscribe_serializer.data)

    def post(self, request):
        can_add = shortcuts.check_permission('add_subscribe', request)
        if can_add:
            serializer = serializers.SubscribeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({'message'  : 'you can not perform this action.'})

    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribe', request)
        if can_update:
            pass
        else:
            return Response({'message'  : 'you can not perform this action.'})

    def delete(self, request, pk):
        can_delete = shortcuts.check_permission('delete_subscribe', request)
        if can_delete:
            pass
        else:
            return Response({'message'  : 'you can not perform this action.'})


class SubscribeOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

class SubscribeContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
