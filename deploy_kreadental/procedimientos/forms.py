from django import forms
from .models import Procedimiento
from especialidades.models import Especialidad

class ProcedimientoForm(forms.ModelForm):
    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.all().order_by('nombre'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Seleccione una especialidad'
        })
    )
    
    class Meta:
        model = Procedimiento
        fields = ['nombre', 'descripcion', 'valor', 'tiempo_estimado', 'estado', 'especialidad']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del procedimiento',
                'required': 'required'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada del procedimiento'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
                'required': 'required'
            }),
            'tiempo_estimado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30',
                'min': '1',
                'required': 'required'
            }),
            'estado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch'
            })
        }
        labels = {
            'nombre': 'Nombre del Procedimiento',
            'descripcion': 'Descripción',
            'valor': 'Valor',
            'tiempo_estimado': 'Tiempo Estimado',
            'estado': 'Estado',
            'especialidad': 'Especialidad'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos requeridos
        for field in ['nombre', 'valor', 'tiempo_estimado', 'especialidad']:
            self.fields[field].required = True