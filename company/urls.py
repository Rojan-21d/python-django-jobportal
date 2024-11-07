from django.urls import path
from . import views

urlpatterns = [
    path('update-company/<int:pk>/', views.UpdateCompanyView.as_view(), name='update-company'),
    path('details/<int:pk>/', views.CompanyDetailView.as_view(), name='company-details')
]
