from django.contrib import admin

from job.models import Category, Experience, State


admin.site.register([Category, State, Experience])
