from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.views import APIView
from XLaw import shortcuts
from rest_framework.permissions import IsAuthenticated

class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class NewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pass

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

class CaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pass

    def post(self, request, pk):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

