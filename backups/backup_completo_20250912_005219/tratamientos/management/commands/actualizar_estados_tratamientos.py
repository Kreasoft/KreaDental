from django.core.management.base import BaseCommand
from django.db.models import Sum
from tratamientos.models import Tratamiento
from pagos_tratamientos.models import PagoTratamiento


class Command(BaseCommand):
    help = 'Actualiza el estado de los tratamientos basado en el total de pagos'

    def handle(self, *args, **options):
        tratamientos = Tratamiento.objects.all()
        actualizados = 0
        
        for tratamiento in tratamientos:
            # Calcular el total pagado
            total_pagado = PagoTratamiento.objects.filter(
                tratamiento=tratamiento,
                estado='COMPLETADO'
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            estado_anterior = tratamiento.estado
            
            # Determinar el estado correcto
            if total_pagado >= tratamiento.costo_total:
                if tratamiento.estado != 'COMPLETADO':
                    tratamiento.estado = 'COMPLETADO'
                    tratamiento.save(update_fields=['estado'])
                    actualizados += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Tratamiento #{tratamiento.id} actualizado a COMPLETADO '
                            f'(Pagado: ${total_pagado}, Total: ${tratamiento.costo_total})'
                        )
                    )
            elif total_pagado > 0:
                if tratamiento.estado not in ['EN_PROGRESO', 'COMPLETADO']:
                    tratamiento.estado = 'EN_PROGRESO'
                    tratamiento.save(update_fields=['estado'])
                    actualizados += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'Tratamiento #{tratamiento.id} actualizado a EN_PROGRESO '
                            f'(Pagado: ${total_pagado}, Total: ${tratamiento.costo_total})'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nProceso completado. {actualizados} tratamientos actualizados.')
        )
