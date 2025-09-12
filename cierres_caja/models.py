from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from pagos_tratamientos.models import PagoTratamiento

# Obtener el modelo de usuario personalizado
User = get_user_model()

class CierreCaja(models.Model):
    fecha = models.DateField(default=timezone.now)
    hora_apertura = models.TimeField(auto_now_add=True)
    hora_cierre = models.TimeField(null=True, blank=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tarjeta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_transferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
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
    pagos = models.ManyToManyField(PagoTratamiento, related_name='cierre_caja')
    
    class Meta:
        verbose_name = 'Cierre de Caja'
        verbose_name_plural = 'Cierres de Caja'
        ordering = ['-fecha', '-hora_apertura']
    
    @property
    def saldo_final(self):
        """Calcula el saldo final del cierre de caja"""
        return self.monto_inicial + self.total_efectivo + self.total_tarjeta + self.total_transferencia + self.diferencia
    
    def __str__(self):
        return f'Cierre de caja {self.fecha} - {self.get_estado_display()}'
