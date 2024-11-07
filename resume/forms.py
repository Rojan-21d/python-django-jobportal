from django import forms
from .models import Resume

class UpdateResumeForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        input_formats=['%d/%m/%Y'],  # Accept DD/MM/YYYY format
        required=False,
        widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'})
    )
    date_from = forms.DateField(
        input_formats=['%d/%m/%Y'],  # Accept DD/MM/YYYY format
        required=False,
        widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'})
    )
    date_to = forms.DateField(
        input_formats=['%d/%m/%Y'],  # Accept DD/MM/YYYY format
        required=False,
        widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'})
    )
    resume_file = forms.FileField(required=True)
        
    class Meta:
        model = Resume
        exclude = ('user',)
