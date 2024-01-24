from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('client/confirm-email/<str:token>/'), # for send email confirmation as client
    path('lawyer/confirm-email/<str:token>/'), # for send email confirmation as lawyer
]
