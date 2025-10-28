from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

# Obtener el modelo de usuario personalizado
User = get_user_model()

class CierreCaja(models.Model):
    fecha = models.DateField(default=timezone.now)
    hora_apertura = models.TimeField(auto_now_add=True)
    hora_cierre = models.TimeField(null=True, blank=True)
    monto_inicial = models.IntegerField(default=0)
    monto_final = models.IntegerField(null=True, blank=True)
    total_efectivo = models.IntegerField(default=0)
    total_tarjeta = models.IntegerField(default=0)
    total_transferencia = models.IntegerField(default=0)
    diferencia = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True)
    usuario_apertura = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cierres_apertura',
        verbose_name='usuario de apertura'
    )
    usuario_cierre = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cierres_cierre',
        null=True,
        blank=True,
        verbose_name='usuario de cierre'
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ('ABIERTO', 'Abierto'),
            ('CERRADO', 'Cerrado')
        ],
        default='ABIERTO'
    )
    # Nota: Los pagos se manejan a través de las vistas, no con relaciones directas
    # debido a que hay múltiples tipos de pagos (PagoTratamiento, PagoAtencion, Pago)
    
    class Meta:
        verbose_name = 'Cierre de Caja'
        verbose_name_plural = 'Cierres de Caja'
        ordering = ['-fecha', '-hora_apertura']
    
    @property
    def saldo_final(self):
        """Calcula el saldo final del cierre de caja"""
        # Fórmula simple: Monto Inicial + Total Pagos - Total Retiros
        total_pagos = self.total_efectivo + self.total_tarjeta + self.total_transferencia
        total_retiros = sum(retiro.monto for retiro in self.retiros.all())
        return self.monto_inicial + total_pagos - total_retiros
    
    @property
    def total_retiros(self):
        """Calcula el total de retiros del día"""
        return sum(retiro.monto for retiro in self.retiros.all())
    
    def __str__(self):
        return f'Cierre de caja {self.fecha} - {self.get_estado_display()}'


class RetiroCaja(models.Model):
    """Modelo para registrar retiros de dinero de la caja para compras especiales"""
    cierre_caja = models.ForeignKey(
        CierreCaja,
        on_delete=models.CASCADE,
        related_name='retiros',
        verbose_name='Cierre de Caja'
    )
    monto = models.IntegerField(verbose_name='Monto del Retiro')
    concepto = models.CharField(
        max_length=200,
        verbose_name='Concepto del Retiro',
        help_text='Descripción del gasto o compra especial'
    )
    fecha_retiro = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora del Retiro'
    )
    usuario_retiro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='retiros_caja',
        verbose_name='Usuario que Retira'
    )
    comprobante = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Número de Comprobante',
        help_text='Número de factura, boleta o comprobante del gasto'
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones Adicionales'
    )
    
    class Meta:
        verbose_name = 'Retiro de Caja'
        verbose_name_plural = 'Retiros de Caja'
        ordering = ['-fecha_retiro']
    
    def __str__(self):
        return f'Retiro ${self.monto:,} - {self.concepto} ({self.fecha_retiro.strftime("%d/%m/%Y %H:%M")})'
