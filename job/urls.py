from django.urls import path
from . import views

urlpatterns = [
    # path('create-job/', views.create_job, name='create-job'),
    path('create-job/', views.CreateJobView.as_view(), name='create-job'),
    # path('update-job/<int:pk>/', views.update_job, name='update-job'),
    path('job/update/<int:pk>/', views.UpdateJobView.as_view(), name='update-job'),
    path('manage-job/', views.ManageJobsView.as_view(), name='manage-job'),
    path('apply/<int:pk>/', views.ApplyToJobView.as_view(), name='apply'),
    path('<int:pk>/applicants/', views.AllApplicantsView.as_view(), name='applicants'),
    path('applied-jobs/', views.AppliedJob.as_view(), name='applied-jobs'),
]
