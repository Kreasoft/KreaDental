from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tratamiento
from pagos_tratamientos.models import PagoTratamiento
from django.db.models import Sum


@receiver(post_save, sender=PagoTratamiento)
def actualizar_estado_tratamiento(sender, instance, created, **kwargs):
    """
    Actualiza el estado del tratamiento cuando se completa un pago
    """
    if instance.estado == 'COMPLETADO':
        tratamiento = instance.tratamiento
        
        # Calcular el total pagado
        total_pagado = PagoTratamiento.objects.filter(
            tratamiento=tratamiento,
            estado='COMPLETADO'
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        # Si el tratamiento está completamente pagado, cambiar estado
        if total_pagado >= tratamiento.costo_total:
            if tratamiento.estado != 'COMPLETADO':
                tratamiento.estado = 'COMPLETADO'
                tratamiento.save(update_fields=['estado'])
        else:
            # Si no está completamente pagado pero tenía estado COMPLETADO, cambiar a EN_PROGRESO
            if tratamiento.estado == 'COMPLETADO' and total_pagado < tratamiento.costo_total:
                tratamiento.estado = 'EN_PROGRESO'
                tratamiento.save(update_fields=['estado'])
