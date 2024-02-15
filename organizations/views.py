from django.shortcuts import render
from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from XLaw import shortcuts
from rest_framework.response import Response
from . import filters
from rest_framework import status

class OrganizationView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        if pk:
            instance = shortcuts.object_is_exist(pk, models.Organization, 'organization not found')
            serializer = serializers.OrganizationSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        queryset = models.Organization.objects.filter(subscribe_contract__is_active=True)
        filter = filters.OrganizationFilter(request.GET, queryset=queryset)
        if filter.is_valid():
            queryset = filter.qs
        serializer = serializers.OrganizationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        can_add = shortcuts.check_permission('add_organization',request)
        if can_add:
            serializer = serializers.OrganizationSerializer(request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message' : 'You can not perform this action'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        can_add = shortcuts.check_permission('change_organization',request)
        instance = shortcuts.object_is_exist(pk, models.Organization, "organizations not found")
        if can_add:
            serializer = serializers.OrganizationSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.pk == instance.user.pk:
            serializer = serializers.OrganizationSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data.pop('subscribe_contract', None)
                serializer.validated_data.pop('user', None)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message' : 'You can not perform this action'})

    def delete(self, request, pk):
        can_add = shortcuts.check_permission('delete_organization',request)
        instance = shortcuts.object_is_exist(pk, models.Organization, "organizations not found")
        if can_add:
            instance.delete()
            return Response({'message':'Organization has been deleted successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'You can not perform this action'}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationStaffView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class PaymentMethodView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

