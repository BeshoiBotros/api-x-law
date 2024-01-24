from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('send-email-confirmation/', views.CustomUserEmail.as_view()), # for send email confirmation as client or Lawyer
    path('client/confirm-email/<str:token>/', views.ClientRegistration.as_view()),
    path('lawyer/confirm-email/<str:token>/', views.LawyerRegistration.as_view()),
]
