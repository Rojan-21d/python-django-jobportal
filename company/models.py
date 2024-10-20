from django.db import models
from users.models import User

class State(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    est_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    services = models.TextField(null=True, blank=True)
    overview = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="company_post_images/%Y/%m/%d", blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name or "No Name"  # Avoids potential NoneType issues
