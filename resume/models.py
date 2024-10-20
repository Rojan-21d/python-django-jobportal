from django.db import models
from job.models import State
from users.models import User


class Resume(models.Model):
    SEX_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other")
    ]
    MARITAL_STATUS_CHOICES = [
        ("unmarried", "Unmarried"),
        ("married", "Married"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, default="other")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default="unmarried")
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True)
    graduation = models.CharField(max_length=100, blank=True, null=True)
    university_college = models.CharField(max_length=100, blank=True, null=True)
    degree_certification = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True)
    course_title = models.CharField(max_length=100, blank=True)
    additional_info = models.TextField(blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    job_position = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True)
    skill_proficiency = models.CharField(max_length=10, blank=True)
    resume_file = models.FileField(upload_to='resume', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
