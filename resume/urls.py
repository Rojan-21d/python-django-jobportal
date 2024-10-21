from django.urls import path
from . import views

urlpatterns = [
    path('update-resume/<int:pk>/', views.UpdateResumeView.as_view(), name='update-resume'),
    path('resume-details/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-details'),
]