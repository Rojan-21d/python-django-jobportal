from django.db import models
from users.models import User

class Company(models.Model):
    STATE_CHOICES = [
        ("Province one", "Province one"),
        ("Province two", "Province two"),
        ("Bagmati", "Bagmati"),
        ("Gandaki", "Gandaki"),
        ("Lumbini", "Lumbini"),
        ("Karnali", "Karnali"),
        ("Sudurpashchim", "Sudurpashchim"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    est_date = models.DateField(null=True, blank=True)  # For storing only the date
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    email = models.EmailField(unique=True, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    services = models.TextField(null=True, blank=True)
    overview = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name or "No Name"  # Avoids potential NoneType issues
