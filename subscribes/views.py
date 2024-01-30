from django.shortcuts import render
from . import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import models
from XLaw import shortcuts
from rest_framework.response import Response
from rest_framework import status

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            subscribe_instance = shortcuts.object_is_exist(pk, models.Subscribe, "subscribe not found")
            subscribe_serializer = serializers.SubscribeSerializer(subscribe_instance)
            return Response(subscribe_serializer.data, status=status.HTTP_200_OK)
        subscribe_queryset = models.Subscribe.objects.all()
        subscribe_serializer = serializers.SubscribeSerializer(subscribe_queryset, many=True)
        return Response(subscribe_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        can_add = shortcuts.check_permission('add_subscribe', request)
        if can_add:
            serializer = serializers.SubscribeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribe', request)
        if can_update:
            instance = shortcuts.object_is_exist(pk, models.Subscribe, "Subscribe not found.")
            serializer = serializers.SubscribeSerializer(instance=instance,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        can_delete = shortcuts.check_permission('delete_subscribe', request)
        if can_delete:
            instance = shortcuts.object_is_exist(pk, models.Subscribe, "Subscribe not found.")
            instance.delete()
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)


class SubscribeOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        can_view = shortcuts.check_permission('view_subscribeorder', request)
        if can_view:
            if pk:
                instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
                serialzier = serializers.SubscribeOrderSerializer(instance)
            else:
                queryset = models.SubscribeOrder.objects.all()
                serialzier = serializers.SubscribeOrderSerializer(queryset, many=True)
            return Response(serialzier.data)
        else:
            return Response({'Message':'you do not have access to perform that action'})
    
    def post(self, request):
        serializer = serializers.SubscribeOrderSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribeorder', request)
        if can_update:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
            serializer = serializers.SubscribeOrderSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({'message':'you do not have access to perform that action'})
        
    def delete(self, request, pk):
        can_delete = shortcuts.check_permission('delete_subscribeorder', request)
        if can_delete:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
            instance.delete()
            return Response({'message' : 'subscribe order has been deleted successfuly'})
        else:
            return Response({'message':'you do not have access to perform that action'})


class SubscribeContractView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        can_view = shortcuts.check_permission('view_subscribecontract', request)
        if can_view:
            if pk:
                instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
                serialzier = serializers.SubscribeContractSerializer(instance)
            else:
                queryset = models.SubscribeContract.objects.all()
                serialzier = serializers.SubscribeContractSerializer(queryset, many=True)
            return Response(serialzier.data)
        else:
            return Response({'message': 'you do not have access to perform that action'})
    
    def post(self, request):
        can_add = shortcuts.check_permission('add_subscribecontract', request)
        if can_add:
            serializer = serializers.SubscribeContractSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({'message': 'you do not have access to perform that action'})

    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribecontract', request)
        if can_update:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
            serializer = serializers.SubscribeContractSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response({'message': 'you do not have access to perform that action'})

    def delete(self, request, pk):
        can_delete = shortcuts.check_permission('delete_subscribecontract', request)
        if can_delete:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
            instance.delete()
            return Response({'Message': 'subscribe contract has been deleted successfully'})
        else:
            return Response({'Message': 'you do not have access to perform that action'})