from django import forms
from .models import Category, Job

class CreateJobForm(forms.ModelForm):
    category_name = forms.CharField(max_length=255, label="Job Category", required=False)  # Text input for new categories
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Select Category")  # Dropdown for existing categories

    class Meta:
        model = Job
        exclude = ('user', 'company')

class UpdateJobForm(forms.ModelForm):
    category_name = forms.CharField(max_length=255, label="Job Category", required=False)  # Text input for new categories
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Select Category")  # Dropdown for existing categories

    class Meta:
        model = Job
        exclude = ('user', 'company')