from django.db import models
from users.models import User
from company.models import Company
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    def get_available_jobs_count(self):
        return Job.objects.filter(
            is_available=True,
            category=self,
        ).count()
        
class State(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("part-time", "Part Time"),
        ("full-time", "Full Time"),
    ]
    EXPERIENCE_CHOICES = [
        ('0', 'Less than 1 year'),
        ('1', '1 year'),
        ('2', '2 years'),
        ('3', '3 years'),
        ('4', '4 years'),
        ('5', '5 years or more'),
    ]
    
    WORK_MODES_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="full-time")
    image = models.ImageField(upload_to="post_images/%y/%m/&=%d", blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    city = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, blank=True, null=True)
    salary = models.PositiveIntegerField(blank=True, null=True)
    work_mode = models.CharField(max_length=20, choices=WORK_MODES_CHOICES, default="onsite")
    edu_level = models.CharField(max_length=255)
    experience = models.CharField(max_length=1, choices=EXPERIENCE_CHOICES)
    uploaded_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    email = models.EmailField(max_length=255)
    contact = models.IntegerField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    
    def application_count(self):
        return self.applyjob_set.count()
    
    def __str__(self):
        return self.title


class ApplyJob(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)