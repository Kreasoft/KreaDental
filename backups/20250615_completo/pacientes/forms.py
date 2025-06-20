from django import forms
from .models import Paciente, HistorialClinico
from profesionales.models import Profesional
from datetime import datetime

class PacienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'max': datetime.now().strftime('%Y-%m-%d')
            }
        ),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Paciente
        fields = ['nombre', 'apellidos', 'documento', 'genero', 'fecha_nacimiento', 
                 'telefono', 'email', 'comuna', 'ciudad', 'direccion', 'prevision', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prevision': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.fecha_nacimiento:
                self.initial['fecha_nacimiento'] = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')

class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = ['tipo', 'descripcion', 'observaciones', 'profesional', 'archivo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profesional': forms.Select(attrs={'class': 'form-select'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'})
        } 