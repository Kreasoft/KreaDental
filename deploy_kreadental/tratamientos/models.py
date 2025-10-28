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
    pagado = models.BooleanField(default=False)
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

    @property
    def monto_pagado(self):
        return sum(pago.monto for pago in self.pagos_realizados.filter(estado='PAGADO'))

    @property
    def monto_pendiente(self):
        return self.costo_total - self.monto_pagado

    def save(self, *args, **kwargs):
        # Primero guardar el tratamiento para obtener el PK
        super().save(*args, **kwargs)
        # Luego calcular y actualizar el costo total
        self.costo_total = self.calcular_costo_total()
        # Actualizar el estado de pago
        self.pagado = self.monto_pendiente == 0
        # Guardar nuevamente con los campos actualizados
        super().save(update_fields=['costo_total', 'pagado'])

class SesionTratamiento(models.Model):
    """Modelo para sesiones individuales de tratamientos"""
    ESTADO_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
        ('NO_ASISTIO', 'No Asistió')
    ]

    tratamiento = models.ForeignKey(
        Tratamiento, 
        on_delete=models.CASCADE, 
        related_name='sesiones'
    )
    numero_sesion = models.PositiveIntegerField(help_text='Número de sesión dentro del tratamiento')
    fecha_programada = models.DateTimeField(help_text='Fecha y hora programada para la sesión')
    fecha_realizada = models.DateTimeField(null=True, blank=True, help_text='Fecha y hora en que se realizó la sesión')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PROGRAMADA')
    costo_sesion = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text='Costo específico de esta sesión'
    )
    observaciones = models.TextField(blank=True, help_text='Observaciones de la sesión')
    profesional = models.ForeignKey(
        'profesionales.Profesional', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='sesiones_atendidas'
    )
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tratamiento', 'numero_sesion']
        verbose_name = 'Sesión de Tratamiento'
        verbose_name_plural = 'Sesiones de Tratamientos'
        unique_together = ['tratamiento', 'numero_sesion']

    def __str__(self):
        return f"Sesión {self.numero_sesion} - {self.tratamiento} - {self.get_estado_display()}"

    @property
    def pagada(self):
        """Verifica si la sesión tiene pagos completados"""
        return self.pagos_sesion.filter(estado='COMPLETADO').exists()

    @property
    def monto_pagado(self):
        """Calcula el monto total pagado por esta sesión"""
        return sum(pago.monto for pago in self.pagos_sesion.filter(estado='COMPLETADO'))

    @property
    def saldo_pendiente(self):
        """Calcula el saldo pendiente de esta sesión"""
        return self.costo_sesion - self.monto_pagado

class DetalleTratamiento(models.Model):
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='detalles')
    procedimiento = models.ForeignKey(Procedimiento, on_delete=models.PROTECT)
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
        if not self.profesional and self.tratamiento and self.tratamiento.profesional:
            self.profesional = self.tratamiento.profesional
            
        super().save(*args, **kwargs)
        # Actualizar costo total del tratamiento
        if self.tratamiento:
            self.tratamiento.save()

class Pago(models.Model):
    METODO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('OTRO', 'Otro')
    ]
    
    ESTADO_CHOICES = [
        ('PAGADO', 'Pagado'),
        ('PENDIENTE', 'Pendiente'),
        ('VENCIDO', 'Vencido')
    ]
    
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='pagos_realizados')
    fecha = models.DateField(default=timezone.now)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PAGADO')
    referencia = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pagos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"Pago de {self.tratamiento.paciente.nombre_completo} - ${self.monto}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar el estado de pago del tratamiento
        self.tratamiento.save() 