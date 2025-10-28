from django import forms
from .models import Laboratorio, TrabajoLaboratorio, SeguimientoTrabajo

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TrabajoLaboratorioForm(forms.ModelForm):
    class Meta:
        model = TrabajoLaboratorio
        fields = ['laboratorio', 'paciente', 'profesional', 'tipo_trabajo', 
                 'descripcion', 'estado', 'fecha_envio', 'fecha_estimada_entrega', 
                 'notas', 'costo']
        widgets = {
            'laboratorio': forms.Select(attrs={'class': 'form-select'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'profesional': forms.Select(attrs={'class': 'form-select'}),
            'tipo_trabajo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_envio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_estimada_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que los campos de fecha sean requeridos
        self.fields['fecha_estimada_entrega'].required = True
        self.fields['descripcion'].required = True

class SeguimientoTrabajoForm(forms.ModelForm):
    MOTIVO_DEVOLUCION_CHOICES = [
        ('', 'Seleccionar motivo...'),
        ('CALIDAD', 'Defecto de calidad'),
        ('MEDIDAS', 'Medidas incorrectas'),
        ('COLOR', 'Color no coincide'),
        ('FUNCION', 'No funciona correctamente'),
        ('ACABADO', 'Acabado defectuoso'),
        ('OTRO', 'Otro motivo'),
    ]
    
    motivo_devolucion = forms.ChoiceField(
        choices=MOTIVO_DEVOLUCION_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_motivo_devolucion'
        }),
        label='Motivo de devolución (si aplica)'
    )
    
    class Meta:
        model = SeguimientoTrabajo
        fields = ['estado', 'notas']
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'id_estado'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Describe el cambio de estado...',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que las notas sean requeridas
        self.fields['notas'].required = True
        self.fields['estado'].required = True
        
        # Agregar JavaScript para mostrar/ocultar motivo de devolución
        self.fields['estado'].widget.attrs['onchange'] = 'toggleMotivoDevolucion()'

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        motivo_devolucion = cleaned_data.get('motivo_devolucion')
        notas = cleaned_data.get('notas')
        
        # Si el estado es DEVUELTO, el motivo de devolución es requerido
        if estado == 'DEVUELTO':
            if not motivo_devolucion:
                self.add_error('motivo_devolucion', 'El motivo de devolución es requerido cuando se devuelve un trabajo.')
            if not notas or len(notas.strip()) < 10:
                self.add_error('notas', 'Las notas deben tener al menos 10 caracteres cuando se devuelve un trabajo.')
        
        return cleaned_data
