from django import forms
from .models import Profesional
from especialidades.models import Especialidad
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from empresa.utils import get_empresa_actual
from empresa.models import Empresa

class ProfesionalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurarse de que las especialidades estén disponibles
        especialidades = Especialidad.objects.filter(estado=True).order_by('nombre')
        print(f"Cargando {especialidades.count()} especialidades")
        
        # Hacer todos los campos requeridos excepto los que pueden ser nulos
        for field_name, field in self.fields.items():
            if field_name not in ['telefono', 'email', 'direccion', 'activo']:
                field.required = True
                field.widget.attrs['required'] = 'required'
        
        self.fields['especialidad'] = forms.ModelChoiceField(
            queryset=especialidades,
            widget=forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            required=True,
            label='Especialidad',
            empty_label='Seleccione una especialidad'
        )

        # Obtener la empresa actual para filtrar las opciones de empresas compartidas
        empresa_actual = None
        if hasattr(self, 'request') and self.request:
            empresa_actual = get_empresa_actual(self.request)
        
        if empresa_actual:
            # Filtrar empresas compartidas para excluir la empresa actual
            self.fields['empresas_compartidas'].queryset = Empresa.objects.filter(
                activa=True
            ).exclude(id=empresa_actual.id)
        else:
            self.fields['empresas_compartidas'].queryset = Empresa.objects.filter(activa=True)

    class Meta:
        model = Profesional
        fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno', 
                 'fecha_nacimiento', 'genero', 'telefono', 'email', 
                 'direccion', 'especialidad', 'activo', 'porcentaje_utilidad',
                 'compartir_entre_sucursales', 'empresas_compartidas']
        
        # Especificar el formato de fecha para el input
        input_formats = {
            'fecha_nacimiento': ['%Y-%m-%d'],
        }
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 11.111.111-1',
                'pattern': '[0-9]{1,2}\.[0-9]{3}\.[0-9]{3}-[0-9kK]{1}',
                'title': 'Formato: 11.111.111-1'
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres'
            }),
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido Paterno'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido Materno'
            }),
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'genero': forms.Select(attrs={
                'class': 'form-select'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'especialidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'porcentaje_utilidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00'
            }),
            'compartir_entre_sucursales': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'empresas_compartidas': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'rut': 'RUT',
            'nombres': 'Nombres',
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'genero': 'Género',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
            'especialidad': 'Especialidad',
            'activo': 'Activo',
            'porcentaje_utilidad': 'Porcentaje de Utilidad (%)',
            'compartir_entre_sucursales': 'Compartir entre sucursales',
            'empresas_compartidas': 'Empresas Compartidas',
        }

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        # Eliminar puntos y guión
        rut = rut.replace('.', '').replace('-', '')
        
        # Validar formato
        if not re.match(r'^[0-9]{8,9}[0-9kK]$', rut):
            raise forms.ValidationError('El RUT debe tener el formato correcto (ej: 11.111.111-1)')
        
        # Validar dígito verificador
        cuerpo = rut[:-1]
        dv = rut[-1].upper()
        
        # Calcular dígito verificador
        suma = 0
        multiplicador = 2
        
        for r in reversed(cuerpo):
            suma += int(r) * multiplicador
            multiplicador = multiplicador + 1 if multiplicador < 7 else 2
        
        dvr = 11 - (suma % 11)
        if dvr == 11:
            dvr = '0'
        elif dvr == 10:
            dvr = 'K'
        else:
            dvr = str(dvr)
        
        if dv != dvr:
            raise forms.ValidationError('El RUT ingresado no es válido')
        
        # Formatear RUT
        rut = f"{cuerpo[:-6]}.{cuerpo[-6:-3]}.{cuerpo[-3:]}-{dv}"
        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        # Eliminar espacios y caracteres especiales
        telefono = re.sub(r'[^0-9+]', '', telefono)
        
        # Validar formato
        if not re.match(r'^\+?[0-9]{8,12}$', telefono):
            raise forms.ValidationError('El teléfono debe tener un formato válido')
        
        return telefono

    def clean_email(self):
        email = self.cleaned_data['email']
        # Si estamos editando un profesional, excluirlo de la búsqueda
        if self.instance and self.instance.pk:
            if Profesional.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado')
        # Si es un nuevo registro, verificar si el correo ya existe
        elif Profesional.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email

    def clean_porcentaje_utilidad(self):
        porcentaje = self.cleaned_data['porcentaje_utilidad']
        if porcentaje is not None:
            if porcentaje < 0:
                raise forms.ValidationError('El porcentaje de utilidad no puede ser negativo')
            if porcentaje > 100:
                raise forms.ValidationError('El porcentaje de utilidad no puede ser mayor a 100%')
        return porcentaje

    def save(self, commit=True):
        try:
            profesional = super().save(commit=False)
            if commit:
                profesional.save()
            return profesional
        except Exception as e:
            print(f"Error al guardar profesional: {str(e)}")
            raise ValidationError(_(f'Error al guardar el profesional: {str(e)}'))

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 