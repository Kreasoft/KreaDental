from django import forms
from .models import Prevision

class PrevisionForm(forms.ModelForm):
    class Meta:
        model = Prevision
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

            
