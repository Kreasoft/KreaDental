from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from tratamientos.models import Tratamiento, SesionTratamiento
from formas_pago.models import FormaPago
from citas.models import Cita

User = get_user_model()

class PagoTratamiento(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('ANULADO', 'Anulado')
    ]

    tratamiento = models.ForeignKey(
        Tratamiento, 
        on_delete=models.PROTECT,
        related_name='pagos'
    )
    forma_pago = models.ForeignKey(
        FormaPago, 
        on_delete=models.PROTECT,
        related_name='pagos_tratamientos'
    )
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Monto del pago'
    )
    fecha_pago = models.DateTimeField(
        default=timezone.now,
        help_text='Fecha y hora en que se realizó el pago'
    )
    comprobante = models.CharField(
        max_length=50, 
        blank=True,
        help_text='Número de comprobante o referencia del pago'
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='PENDIENTE'
    )
    notas = models.TextField(
        blank=True,
        help_text='Notas adicionales sobre el pago'
    )
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='pagos_tratamientos_creados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = 'Pago de Tratamiento'
        verbose_name_plural = 'Pagos de Tratamientos'

    def __str__(self):
        return f"Pago {self.id} - {self.tratamiento} - ${self.monto}"

    def save(self, *args, **kwargs):
        # Validar que el monto no sea negativo
        if self.monto < 0:
            raise ValueError("El monto del pago no puede ser negativo")

        # Validar que el monto no exceda el saldo pendiente
        saldo_pendiente = self.tratamiento.costo_total - sum(
            pago.monto for pago in self.tratamiento.pagos.exclude(id=self.id)
            if pago.estado == 'COMPLETADO'
        )
        
        if self.monto > saldo_pendiente and self.estado == 'COMPLETADO':
            raise ValueError(
                f"El monto del pago (${self.monto}) excede el saldo pendiente (${saldo_pendiente})"
            )

        super().save(*args, **kwargs)

class PagoAtencion(models.Model):
    """Modelo para pagos de atenciones únicas (citas)"""
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('ANULADO', 'Anulado')
    ]

    TIPO_PAGO_CHOICES = [
        ('ATENCION_UNICA', 'Atención Única'),
        ('SESION_TRATAMIENTO', 'Sesión de Tratamiento'),
        ('CONSULTA', 'Consulta'),
        ('URGENCIA', 'Urgencia')
    ]

    cita = models.ForeignKey(
        Cita, 
        on_delete=models.PROTECT,
        related_name='pagos_atencion'
    )
    forma_pago = models.ForeignKey(
        FormaPago, 
        on_delete=models.PROTECT,
        related_name='pagos_atenciones'
    )
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Monto del pago'
    )
    tipo_pago = models.CharField(
        max_length=20,
        choices=TIPO_PAGO_CHOICES,
        default='ATENCION_UNICA',
        help_text='Tipo de atención pagada'
    )
    fecha_pago = models.DateTimeField(
        default=timezone.now,
        help_text='Fecha y hora en que se realizó el pago'
    )
    comprobante = models.CharField(
        max_length=50, 
        blank=True,
        help_text='Número de comprobante o referencia del pago'
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='PENDIENTE'
    )
    notas = models.TextField(
        blank=True,
        help_text='Notas adicionales sobre el pago'
    )
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='pagos_atenciones_creados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = 'Pago de Atención'
        verbose_name_plural = 'Pagos de Atenciones'

    def __str__(self):
        return f"Pago Atención {self.id} - {self.cita} - ${self.monto}"

    def save(self, *args, **kwargs):
        # Validar que el monto no sea negativo
        if self.monto < 0:
            raise ValueError("El monto del pago no puede ser negativo")

        super().save(*args, **kwargs)

class PagoSesion(models.Model):
    """Modelo para pagos de sesiones individuales de tratamientos"""
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('ANULADO', 'Anulado')
    ]

    sesion = models.ForeignKey(
        SesionTratamiento, 
        on_delete=models.PROTECT,
        related_name='pagos_sesion'
    )
    forma_pago = models.ForeignKey(
        FormaPago, 
        on_delete=models.PROTECT,
        related_name='pagos_sesiones'
    )
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Monto del pago'
    )
    fecha_pago = models.DateTimeField(
        default=timezone.now,
        help_text='Fecha y hora en que se realizó el pago'
    )
    comprobante = models.CharField(
        max_length=50, 
        blank=True,
        help_text='Número de comprobante o referencia del pago'
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='PENDIENTE'
    )
    notas = models.TextField(
        blank=True,
        help_text='Notas adicionales sobre el pago'
    )
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='pagos_sesiones_creados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = 'Pago de Sesión'
        verbose_name_plural = 'Pagos de Sesiones'

    def __str__(self):
        return f"Pago Sesión {self.id} - {self.sesion} - ${self.monto}"

    def save(self, *args, **kwargs):
        # Validar que el monto no sea negativo
        if self.monto < 0:
            raise ValueError("El monto del pago no puede ser negativo")

        # Validar que el monto no exceda el saldo pendiente de la sesión
        saldo_pendiente = self.sesion.saldo_pendiente
        if self.monto > saldo_pendiente and self.estado == 'COMPLETADO':
            raise ValueError(
                f"El monto del pago (${self.monto}) excede el saldo pendiente de la sesión (${saldo_pendiente})"
            )

        super().save(*args, **kwargs)

class HistorialPago(models.Model):
    TIPO_CHOICES = [
        ('CREACION', 'Creación'),
        ('MODIFICACION', 'Modificación'),
        ('ANULACION', 'Anulación')
    ]

    pago = models.ForeignKey(
        PagoTratamiento, 
        on_delete=models.CASCADE,
        related_name='historial'
    )
    tipo_accion = models.CharField(
        max_length=20, 
        choices=TIPO_CHOICES
    )
    estado_anterior = models.CharField(
        max_length=20, 
        blank=True,
        null=True
    )
    estado_nuevo = models.CharField(
        max_length=20
    )
    monto_anterior = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    monto_nuevo = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    notas = models.TextField(
        blank=True
    )
    realizado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT
    )
    fecha_accion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_accion']
        verbose_name = 'Historial de Pago'
        verbose_name_plural = 'Historial de Pagos'

    def __str__(self):
        return f"{self.tipo_accion} - Pago {self.pago.id} - {self.fecha_accion}"