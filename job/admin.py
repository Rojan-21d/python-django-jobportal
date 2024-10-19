from django.contrib import admin

from job.models import Category, State

# Register your models here.


admin.site.register([Category, State])
