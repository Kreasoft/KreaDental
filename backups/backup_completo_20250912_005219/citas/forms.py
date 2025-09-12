from django import forms
from .models import Cita
from datetime import datetime, time, timedelta
from empresa.utils import get_empresa_actual
import re
from profesionales.models import Profesional
from pacientes.models import Paciente

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'profesional', 'fecha', 'hora', 'duracion', 'estado', 'motivo']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': datetime.now().strftime('%Y-%m-%d')
                }
            ),
            'hora': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'min': '08:00',
                    'max': '20:00',
                    'step': '900'  # 15 minutos
                }
            ),
            'duracion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '15',
                'step': '15',
                'value': '30'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required',
                'data-placeholder': 'Buscar paciente...',
                'style': 'width: 100%'
            }),
            'profesional': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer estado por defecto para nuevas citas
        if not self.instance.pk:  # Si es una nueva cita
            self.initial['estado'] = 'PENDIENTE'
        
        # Hacer los campos requeridos
        self.fields['paciente'].required = True
        self.fields['profesional'].required = True
        self.fields['fecha'].required = True
        self.fields['hora'].required = True
        self.fields['duracion'].required = True
        
        # Filtrar profesionales y pacientes por empresa actual
        # Obtener la empresa actual (esto se maneja en la vista)
        # Los querysets se filtran en la vista que pasa el formulario

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            if fecha < datetime.now().date():
                raise forms.ValidationError('La fecha no puede ser anterior a hoy')
        return fecha

    def clean_hora(self):
        hora = self.cleaned_data.get('hora')
        if hora:
            try:
                # Si la hora viene como string, intentar convertirlo a objeto time
                if isinstance(hora, str):
                    try:
                        # Intentar parsear con diferentes formatos
                        for fmt in ['%H:%M:%S', '%H:%M']:
                            try:
                                hora = datetime.strptime(hora, fmt).time()
                                break
                            except ValueError:
                                continue
                        else:
                            raise ValueError('Formato de hora inválido')
                    except ValueError:
                        raise forms.ValidationError('Formato de hora inválido. Use HH:MM o HH:MM:SS')
                
                # Asegurar que los segundos sean válidos
                if hora.second >= 60:
                    raise forms.ValidationError('Los segundos deben estar entre 0 y 59')
                
                # Validar que la hora esté dentro del rango permitido
                hora_min = time(8, 0)  # 8:00 AM
                hora_max = time(20, 0)  # 8:00 PM
                if hora < hora_min or hora > hora_max:
                    raise forms.ValidationError('La hora debe estar entre las 8:00 y las 20:00')
                
                # Validar que la hora sea en intervalos de 15 minutos
                if hora.minute % 15 != 0:
                    raise forms.ValidationError('La hora debe ser en intervalos de 15 minutos')
                
                # Redondear los segundos a 0
                hora = time(hora.hour, hora.minute, 0)
                
            except (AttributeError, ValueError) as e:
                raise forms.ValidationError('Formato de hora inválido. Use HH:MM')
            
        return hora

    def clean_duracion(self):
        duracion = self.cleaned_data.get('duracion')
        if duracion:
            if duracion < 15 or duracion > 120:
                raise forms.ValidationError('La duración debe estar entre 15 y 120 minutos')
            if duracion % 15 != 0:
                raise forms.ValidationError('La duración debe ser múltiplo de 15 minutos')
        return duracion

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        duracion = cleaned_data.get('duracion')
        profesional = cleaned_data.get('profesional')

        if fecha and hora and duracion and profesional:
            # Calcular hora de fin
            hora_inicio = datetime.combine(fecha, hora)
            hora_fin = hora_inicio + timedelta(minutes=duracion)

            # Verificar si hay citas solapadas
            citas_solapadas = Cita.objects.filter(
                profesional=profesional,
                fecha=fecha,
                hora__lt=hora_fin.time(),
                hora__gt=hora
            ).exclude(pk=self.instance.pk if self.instance.pk else None)

            if citas_solapadas.exists():
                raise forms.ValidationError('Ya existe una cita programada en ese horario para este profesional')

        return cleaned_data 