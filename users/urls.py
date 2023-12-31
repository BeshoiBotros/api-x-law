from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('client-register/', views.ClientRegister.as_view()),
    path('client-login/', TokenObtainPairView.as_view())
]
