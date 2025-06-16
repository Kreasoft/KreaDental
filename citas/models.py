from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from pacientes.models import Paciente
from profesionales.models import Profesional
from empresa.models import Empresa

class Cita(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='citas', null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    duracion = models.IntegerField(default=30)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    motivo = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"Cita de {self.paciente} con {self.profesional} el {self.fecha} a las {self.hora}"

    def get_hora_fin(self):
        inicio = datetime.combine(self.fecha, self.hora)
        fin = inicio + timedelta(minutes=self.duracion)
        return fin.time() 