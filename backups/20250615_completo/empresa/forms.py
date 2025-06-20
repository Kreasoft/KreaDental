from django import forms
from .models import Empresa
from django.core.validators import RegexValidator

class EmpresaForm(forms.ModelForm):
    fecha_inicio_licencia = forms.DateField(
        label='Fecha de Inicio de Licencia',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': True
        })
    )
    
    fecha_fin_licencia = forms.DateField(
        label='Fecha de Fin de Licencia',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': True
        })
    )
    
    # Validación personalizada para el RUT
    ruc = forms.CharField(
        label='RUT',
        max_length=20,
        validators=[
            RegexValidator(
                regex='^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]$',
                message='El RUT debe tener el formato: 12.345.678-9',
                code='invalid_rut'
            ),
        ],
        help_text='Formato: 12.345.678-9',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9',
            'data-mask': '00.000.000-0',
            'data-mask-reverse': 'true',
        })
    )

    class Meta:
        model = Empresa
        fields = [
            'razon_social', 'nombre_fantasia', 'ruc', 'direccion', 'telefono', 'email', 'web',
            'logo', 'representante_legal', 'fecha_inicio_licencia', 'fecha_fin_licencia'
        ]
        widgets = {
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razón social completa',
                'required': True
            }),
            'nombre_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre comercial de la empresa',
                'required': True
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@empresa.com',
                'required': True
            }),
            'web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.empresa.com',
            }),
            'representante_legal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del representante legal',
                'required': True
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }