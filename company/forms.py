from django import forms
from .models import Company

class UpdateCompanyForm(forms.ModelForm):
    est_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control resume',
                'placeholder': 'DD/MM/YYYY', 
            }
        ),
        input_formats=['%d/%m/%Y'],  # Accept only DD/MM/YYYY format
        error_messages={
            'invalid': 'Enter a valid date in DD/MM/YYYY format.',
        }
    )
        
    class Meta:
        model = Company
        exclude = ('user', 'is_verified')
        # widgets = {
        #     'services': forms.Textarea(attrs={'rows': 4}),
        #     'overview': forms.Textarea(attrs={'rows': 6}),
        # }
