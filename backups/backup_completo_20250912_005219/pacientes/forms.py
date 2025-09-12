from django import forms
from .models import Paciente, HistorialClinico
from profesionales.models import Profesional
from datetime import datetime
from empresa.utils import get_empresa_actual

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
                 'telefono', 'email', 'comuna', 'ciudad', 'direccion', 'prevision', 'activo',
                 'compartir_entre_sucursales', 'empresas_compartidas']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'prevision': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'compartir_entre_sucursales': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'empresas_compartidas': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.fecha_nacimiento:
                self.initial['fecha_nacimiento'] = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')

        # Obtener la empresa actual para filtrar las opciones de empresas compartidas
        from empresa.models import Empresa
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

class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = ['tipo', 'descripcion', 'observaciones', 'profesional', 'archivo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profesional': forms.Select(attrs={'class': 'form-select'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar profesionales por empresa actual y estado activo
        from empresa.utils import get_empresa_actual
        from django.db.models import Q
        
        empresa_actual = None
        if hasattr(self, 'request') and self.request:
            empresa_actual = get_empresa_actual(self.request)
        
        if empresa_actual:
            profesionales = Profesional.objects.filter(
                Q(empresa=empresa_actual, activo=True) | 
                Q(empresas_compartidas=empresa_actual, compartir_entre_sucursales=True, activo=True)
            ).distinct().order_by('apellido_paterno', 'apellido_materno', 'nombres')
            self.fields['profesional'].queryset = profesionales
        # Los querysets se filtran en las vistas que usan este formulario 