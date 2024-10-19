from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path('job-list/', views.JobListingView.as_view(), name='job-list'),
    path('job-details/<int:pk>/', views.JobDetailView.as_view(), name='job-details'),
]