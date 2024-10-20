from django.contrib import admin
from .models import Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_verified')
    list_editable = ('is_verified',)

admin.site.register(Company, CompanyAdmin)
