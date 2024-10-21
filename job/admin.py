from django.contrib import admin

from job.models import ApplyJob, Category, Experience, State


admin.site.register([Category, State, Experience, ApplyJob])
