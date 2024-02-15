from django.shortcuts import render
from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from XLaw import shortcuts
from rest_framework.response import Response
from . import filters

class OrganizationView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        if pk:
            instance = shortcuts.object_is_exist(pk, models.Organization, 'organization not found')
            serializer = serializers.OrganizationSerializer(instance)
            return Response(serializer.data)
        
        queryset = models.Organization.objects.filter(subscribe_contract__is_active=True)
        filter = filters.OrganizationFilter(request.GET, queryset=queryset)
        if filter.is_valid():
            queryset = filter.qs
        serializer = serializers.OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        can_add = shortcuts.check_permission('add_organization',request)
        if can_add:
            pass
        else:
            return Response({'message' : 'You can not perform this action'})

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


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

