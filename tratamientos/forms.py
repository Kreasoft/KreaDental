from django import forms
from django.forms import inlineformset_factory
from .models import Tratamiento, DetalleTratamiento, Pago
from datetime import date
from django.contrib.auth import get_user_model
from procedimientos.models import Procedimiento
from decimal import Decimal
from pacientes.models import Paciente
from profesionales.models import Profesional

User = get_user_model()

class DetalleTratamientoForm(forms.ModelForm):
    class Meta:
        model = DetalleTratamiento
        fields = ['procedimiento', 'cantidad', 'descuento', 'profesional']
        widgets = {
            'procedimiento': forms.Select(attrs={
                'class': 'form-control procedimiento-select',
                'data-precio': 'valor'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control cantidad',
                'min': '1',
                'value': '1'
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control descuento',
                'min': '0',
                'max': '100',
                'value': '0'
            }),
            'profesional': forms.Select(attrs={
                'class': 'form-control profesional-select',
                'required': 'required'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['procedimiento'].queryset = Procedimiento.objects.all().order_by('nombre')
        self.fields['profesional'].queryset = Profesional.objects.filter(
            activo=True
        ).order_by('apellido_paterno', 'apellido_materno', 'nombres')
        
        # Hacer todos los campos requeridos
        for field_name in ['procedimiento', 'profesional', 'cantidad', 'descuento']:
            self.fields[field_name].required = True
            self.fields[field_name].widget.attrs['required'] = 'required'
            if field_name == 'profesional':
                self.fields[field_name].error_messages = {
                    'required': 'Debe seleccionar un profesional',
                    'invalid_choice': 'El profesional seleccionado no es válido'
                }

        # Agregar el valor del procedimiento como atributo data
        if self.instance and self.instance.pk and self.instance.procedimiento:
            self.fields['procedimiento'].widget.attrs['data-precio'] = str(self.instance.procedimiento.valor)

    def clean_profesional(self):
        profesional = self.cleaned_data.get('profesional')
        if not profesional:
            raise forms.ValidationError('Debe seleccionar un profesional')
        if not profesional.activo:
            raise forms.ValidationError('El profesional seleccionado no está activo')
        return profesional

    def clean(self):
        cleaned_data = super().clean()
        procedimiento = cleaned_data.get('procedimiento')
        cantidad = cleaned_data.get('cantidad')
        descuento = cleaned_data.get('descuento')

        if procedimiento and cantidad and descuento:
            if cantidad < 1:
                raise forms.ValidationError('La cantidad debe ser mayor a 0')
            if descuento < 0 or descuento > 100:
                raise forms.ValidationError('El descuento debe estar entre 0 y 100')

        return cleaned_data

class TratamientoForm(forms.ModelForm):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar pacientes por nombre y apellidos
        self.fields['paciente'].queryset = Paciente.objects.all().order_by('nombre', 'apellidos')
        
        # Ordenar profesionales por apellidos y nombres
        self.fields['profesional'].queryset = Profesional.objects.filter(activo=True).order_by('apellido_paterno', 'apellido_materno', 'nombres')
        
        # Hacer todos los campos requeridos excepto los que pueden ser nulos
        for field_name, field in self.fields.items():
            if field_name not in ['fecha_fin', 'observaciones']:
                field.required = True
                field.widget.attrs['required'] = 'required'
        
        # Configurar widgets con valores iniciales
        self.fields['paciente'].widget = forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
        
        self.fields['profesional'].widget = forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
        
        self.fields['fecha_inicio'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': 'required'
        })
        
        self.fields['fecha_fin'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
        
        self.fields['estado'].widget = forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
        self.fields['estado'].choices = self.ESTADO_CHOICES
        
        self.fields['observaciones'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        })

        # Si estamos editando, asegurarnos de que los valores iniciales estén establecidos
        if self.instance.pk:
            if self.instance.fecha_inicio:
                self.initial['fecha_inicio'] = self.instance.fecha_inicio.strftime('%Y-%m-%d')
            if self.instance.fecha_fin:
                self.initial['fecha_fin'] = self.instance.fecha_fin.strftime('%Y-%m-%d')
            self.initial['estado'] = self.instance.estado
            self.initial['observaciones'] = self.instance.observaciones
            self.initial['profesional'] = self.instance.profesional

    class Meta:
        model = Tratamiento
        fields = ['paciente', 'profesional', 'fecha_inicio', 'fecha_fin', 'estado', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        estado = cleaned_data.get('estado')

        if not paciente:
            self.add_error('paciente', 'Debe seleccionar un paciente')
        if not fecha_inicio:
            self.add_error('fecha_inicio', 'La fecha de inicio es obligatoria')
        if not estado:
            self.add_error('estado', 'Debe seleccionar un estado')
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a la fecha de inicio')

        return cleaned_data

class DetalleTratamientoFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in self.forms):
            raise forms.ValidationError('Debe agregar al menos un procedimiento')
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if not form.cleaned_data.get('profesional'):
                    raise forms.ValidationError('Debe asignar un profesional a cada procedimiento')

# Factory para el formset de detalles
DetalleTratamientoFormSet = inlineformset_factory(
    Tratamiento,
    DetalleTratamiento,
    form=DetalleTratamientoForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=10,
    validate_max=True,
    fields=['procedimiento', 'profesional', 'cantidad', 'descuento']
)

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['tratamiento', 'fecha', 'monto', 'metodo_pago', 'estado', 'referencia', 'notas']
        widgets = {
            'tratamiento': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer todos los campos requeridos excepto referencia y notas
        for field_name in ['tratamiento', 'fecha', 'monto', 'metodo_pago', 'estado']:
            self.fields[field_name].required = True
            self.fields[field_name].widget.attrs['required'] = 'required'

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a 0')
        return monto 