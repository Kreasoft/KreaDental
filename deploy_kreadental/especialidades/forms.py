from django import forms
from .models import Especialidad

class EspecialidadForm(forms.ModelForm):
    estado = forms.BooleanField(
        required=False,
        initial=True,
        label='Activo',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'role': 'switch'
        })
    )

    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 