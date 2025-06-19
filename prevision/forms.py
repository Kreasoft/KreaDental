from django import forms
from .models import Prevision

class PrevisionForm(forms.ModelForm):
    class Meta:
        model = Prevision
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'dental-form-control',
                'placeholder': 'Ingrese el nombre de la previsión',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'dental-form-control dental-textarea',
                'placeholder': 'Ingrese una descripción (opcional)',
                'rows': 4
            }),
            'estado': forms.CheckboxInput(attrs={
                'class': 'dental-switch-input'
            }),
        }

            
