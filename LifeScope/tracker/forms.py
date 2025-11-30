from django import forms
from .models import LifestyleData

class LifestyleDataForm(forms.ModelForm):
    class Meta:
        model = LifestyleData
        fields = ['date', 'steps', 'sleep_hours', 'calories']
        exclude = ['user']


