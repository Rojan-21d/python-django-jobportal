from django.urls import path
from . import views

urlpatterns = [
    # path('update-company/', views.update_company, name='update-company'),
    path('update-company/', views.UpdateCompanyView.as_view(), name='update-company'),
    path('company-details/<int:pk>/', views.company_details, name='company-details'),
]
