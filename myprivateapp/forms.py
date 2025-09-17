from django import forms
from .models import Color

class EditColor(forms.ModelForm):

    class Meta:
        model = Color
        fields = ('id', 'name', 'value',)