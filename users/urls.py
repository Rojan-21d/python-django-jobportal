from django.urls import path
from .views import RegisterApplicantView, RegisterRecruiterView, LoginUserView, logout_user
from . import views

urlpatterns = [
    path('register-applicant/', RegisterApplicantView.as_view(), name='register-applicant'),
    path('register-recruiter/', RegisterRecruiterView.as_view(), name='register-recruiter'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]