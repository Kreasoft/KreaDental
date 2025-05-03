from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pagos_tratamientos.models import PagoTratamiento

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
        User,
        on_delete=models.PROTECT,
        related_name='cierres_apertura'
    )
    usuario_cierre = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='cierres_cierre',
        null=True,
        blank=True
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
    
    def __str__(self):
        return f'Cierre de caja {self.fecha} - {self.get_estado_display()}'
