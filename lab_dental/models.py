from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from pacientes.models import Paciente
from profesionales.models import Profesional

User = get_user_model()

class Laboratorio(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField()
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
        ordering = ['nombre']

class TrabajoLaboratorio(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente de envío'),
        ('ENVIADO', 'Enviado al laboratorio'),
        ('EN_PROCESO', 'En proceso'),
        ('LISTO', 'Listo para recoger'),
        ('RECIBIDO', 'Recibido en clínica'),
        ('ENTREGADO', 'Entregado al paciente'),
        ('CANCELADO', 'Cancelado'),
    ]

    TIPO_TRABAJO_CHOICES = [
        ('CORONA', 'Corona'),
        ('PUENTE', 'Puente'),
        ('PROTESIS', 'Prótesis'),
        ('IMPLANTE', 'Implante'),
        ('OTRO', 'Otro'),
    ]

    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.PROTECT, related_name='trabajos')
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='trabajos_laboratorio')
    profesional = models.ForeignKey(Profesional, on_delete=models.PROTECT, related_name='trabajos_laboratorio')
    tipo_trabajo = models.CharField(max_length=20, choices=TIPO_TRABAJO_CHOICES)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_envio = models.DateField(null=True, blank=True)
    fecha_estimada_entrega = models.DateField()
    fecha_recepcion = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo_trabajo} - {self.paciente} ({self.estado})"

    class Meta:
        verbose_name = "Trabajo de Laboratorio"
        verbose_name_plural = "Trabajos de Laboratorio"
        ordering = ['-fecha_creacion']

class SeguimientoTrabajo(models.Model):
    trabajo = models.ForeignKey(TrabajoLaboratorio, on_delete=models.CASCADE, related_name='seguimientos')
    estado = models.CharField(max_length=20, choices=TrabajoLaboratorio.ESTADO_CHOICES)
    notas = models.TextField()
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trabajo} - {self.estado} ({self.fecha_creacion.strftime('%d/%m/%Y')})"

    class Meta:
        verbose_name = "Seguimiento de Trabajo"
        verbose_name_plural = "Seguimientos de Trabajos"
        ordering = ['-fecha_creacion']
