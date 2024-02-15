from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.OrganizationView.as_view()),
    path('', views.OrganizationView.as_view()),
]