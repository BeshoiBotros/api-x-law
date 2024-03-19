from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.OrganizationView.as_view()),
    path('', views.OrganizationView.as_view()),
    
    path('ownership/<int:pk>/', views.ObjectOwnershipView.as_view()),
    path('ownership/', views.ObjectOwnershipView.as_view()),
    path('ownership/organization/<int:organization_pk>/', views.ObjectOwnershipView.as_view()),
    path('ownership/content/<int:content_type_pk>/', views.ObjectOwnershipView.as_view()),

    

]