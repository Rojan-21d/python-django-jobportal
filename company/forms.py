from django import forms
from .models import Company

class UpdateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user',)
        widgets = {
            'services': forms.Textarea(attrs={'rows': 4}),
            'overview': forms.Textarea(attrs={'rows': 6}),
        }
