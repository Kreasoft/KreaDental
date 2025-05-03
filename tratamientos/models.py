from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from pacientes.models import Paciente
from procedimientos.models import Procedimiento
from decimal import Decimal

User = get_user_model()

class Tratamiento(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='tratamientos')
    profesional = models.ForeignKey('profesionales.Profesional', on_delete=models.SET_NULL, null=True, related_name='tratamientos_asignados')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    observaciones = models.TextField(blank=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tratamientos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'

    def __str__(self):
        return f"Tratamiento de {self.paciente.nombre} {self.paciente.apellidos} - {self.estado}"

    def calcular_costo_total(self):
        total = sum(detalle.total for detalle in self.detalles.all())
        return total

    def save(self, *args, **kwargs):
        # Primero guardar el tratamiento para obtener el PK
        super().save(*args, **kwargs)
        # Luego calcular y actualizar el costo total
        self.costo_total = self.calcular_costo_total()
        # Guardar nuevamente con el costo total actualizado
        super().save(update_fields=['costo_total'])

class DetalleTratamiento(models.Model):
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='detalles')
    procedimiento = models.ForeignKey(Procedimiento, on_delete=models.CASCADE)
    profesional = models.ForeignKey(
        'profesionales.Profesional', 
        on_delete=models.SET_NULL, 
        related_name='detalles_tratamiento',
        null=True,
        blank=True
    )
    cantidad = models.PositiveIntegerField(default=1)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Detalle de Tratamiento'
        verbose_name_plural = 'Detalles de Tratamiento'

    def __str__(self):
        return f"{self.procedimiento} - {self.cantidad}"

    @property
    def subtotal(self):
        return self.procedimiento.valor * self.cantidad

    @property
    def descuento_monto(self):
        return (self.subtotal * self.descuento) / 100

    @property
    def total(self):
        return self.subtotal - self.descuento_monto

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo registro
            self.fecha_creacion = timezone.now()
        self.fecha_actualizacion = timezone.now()
        
        # Si no hay profesional asignado, usar el profesional principal del tratamiento
        if not self.profesional and self.tratamiento:
            self.profesional = self.tratamiento.profesional
            
        super().save(*args, **kwargs)
        # Actualizar costo total del tratamiento si es necesario
        self.tratamiento.save() 