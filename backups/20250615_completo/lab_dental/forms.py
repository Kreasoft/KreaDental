from django import forms
from .models import Laboratorio, TrabajoLaboratorio, SeguimientoTrabajo

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TrabajoLaboratorioForm(forms.ModelForm):
    class Meta:
        model = TrabajoLaboratorio
        fields = ['laboratorio', 'paciente', 'profesional', 'tipo_trabajo', 
                 'descripcion', 'estado', 'fecha_envio', 'fecha_estimada_entrega', 
                 'fecha_recepcion', 'notas', 'costo']
        widgets = {
            'laboratorio': forms.Select(attrs={'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'profesional': forms.Select(attrs={'class': 'form-control'}),
            'tipo_trabajo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_envio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_estimada_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_recepcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SeguimientoTrabajoForm(forms.ModelForm):
    class Meta:
        model = SeguimientoTrabajo
        fields = ['estado', 'notas']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
