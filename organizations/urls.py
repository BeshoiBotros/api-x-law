from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.OrganizationView.as_view()),
    path('', views.OrganizationView.as_view()),
    path('staff/<int:pk>/', views.ObjectOwnershipView.as_view()),
    path('staff/<int:organization_pk>/', views.ObjectOwnershipView.as_view()),
    path('staff/', views.ObjectOwnershipView.as_view())
]