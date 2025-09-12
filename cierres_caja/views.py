from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models
from django.db.models import Sum, Count
from decimal import Decimal
from datetime import timedelta
from .models import CierreCaja
from .forms import CierreCajaForm, CerrarCajaForm
from pagos_tratamientos.models import PagoTratamiento
from formas_pago.models import FormaPago

@login_required
def lista_cierres(request):
    # Obtener fechas para filtrado
    hoy = timezone.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)

    # Obtener parámetros de filtrado
    fecha_inicio = request.GET.get('fecha_desde', inicio_semana.strftime('%Y-%m-%d'))
    fecha_fin = request.GET.get('fecha_hasta', fin_semana.strftime('%Y-%m-%d'))
    estado = request.GET.get('estado', '')

    # Filtrar cierres
    cierres = CierreCaja.objects.all()
    
    if fecha_inicio:
        cierres = cierres.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        cierres = cierres.filter(fecha__lte=fecha_fin)
    if estado:
        cierres = cierres.filter(estado=estado)

    # Ordenar por fecha y hora
    cierres = cierres.order_by('-fecha', '-hora_apertura')

    # Calcular estadísticas
    total_cierres = cierres.count()
    
    # Calcular totales por separado
    total_efectivo = cierres.aggregate(total=Sum('total_efectivo'))['total'] or Decimal('0')
    total_tarjeta = cierres.aggregate(total=Sum('total_tarjeta'))['total'] or Decimal('0')
    total_transferencia = cierres.aggregate(total=Sum('total_transferencia'))['total'] or Decimal('0')
    total_ingresos = total_efectivo + total_tarjeta + total_transferencia
    
    total_egresos = Decimal('0')  # Por ahora no hay egresos en el modelo
    saldo_actual = total_ingresos - total_egresos

    hay_caja_abierta = CierreCaja.objects.filter(estado='ABIERTO').exists()

    return render(request, 'cierres_caja/lista_cierres.html', {
        'cierres': cierres,
        'hay_caja_abierta': hay_caja_abierta,
        'fecha_desde': fecha_inicio,
        'fecha_hasta': fecha_fin,
        'estado': estado,
        'total_cierres': total_cierres,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'saldo_actual': saldo_actual
    })

@login_required
def abrir_caja(request):
    # Verificar si ya hay una caja abierta
    caja_abierta = CierreCaja.objects.filter(estado='ABIERTO').first()
    if caja_abierta:
        messages.error(request, 'Ya hay una caja abierta')
        return redirect('cierres_caja:lista_cierres')
    
    if request.method == 'POST':
        form = CierreCajaForm(request.POST)
        if form.is_valid():
            cierre = form.save(commit=False)
            cierre.usuario_apertura = request.user
            cierre.save()
            messages.success(request, 'Caja abierta exitosamente')
            return redirect('cierres_caja:lista_cierres')
    else:
        form = CierreCajaForm()
    
    return render(request, 'cierres_caja/form_cierre.html', {
        'form': form,
        'accion': 'Abrir'
    })

@login_required
def cerrar_caja(request, cierre_id):
    cierre = get_object_or_404(CierreCaja, id=cierre_id, estado='ABIERTO')
    
    # Obtener todas las formas de pago activas
    formas_pago = FormaPago.objects.filter(estado=True)
    
    # Obtener los pagos del día
    pagos_dia = PagoTratamiento.objects.filter(
        fecha_pago__date=cierre.fecha,
        estado='COMPLETADO'
    )
    
    # Calcular totales por forma de pago
    totales_por_forma = {}
    total_sistema = Decimal('0')
    
    for forma in formas_pago:
        total = pagos_dia.filter(forma_pago=forma).aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0')
        totales_por_forma[forma.nombre] = total
        total_sistema += total
    
    # Agrupar pagos por forma de pago para el resumen
    resumen_pagos = pagos_dia.values('forma_pago__nombre').annotate(
        total=Sum('monto'),
        cantidad=Count('id')
    ).order_by('forma_pago__nombre')
    
    if request.method == 'POST':
        form = CerrarCajaForm(request.POST, instance=cierre)
        if form.is_valid():
            cierre = form.save(commit=False)
            
            # Guardar los totales por forma de pago
            for nombre, total in totales_por_forma.items():
                if nombre == 'EFECTIVO':
                    cierre.total_efectivo = total
                elif nombre == 'TARJETA':
                    cierre.total_tarjeta = total
                elif nombre == 'TRANSFERENCIA':
                    cierre.total_transferencia = total
            
            # Calcular diferencia
            if cierre.monto_final is not None:
                cierre.diferencia = cierre.monto_final - (cierre.monto_inicial + total_sistema)
            else:
                cierre.diferencia = Decimal('0')  # Establecer un valor por defecto
            
            # Actualizar estado y usuario
            cierre.estado = 'CERRADO'
            cierre.usuario_cierre = request.user
            cierre.hora_cierre = timezone.now().time()
            
            # Guardar pagos asociados
            cierre.save()
            cierre.pagos.set(pagos_dia)
            
            messages.success(request, 'Caja cerrada exitosamente')
            return redirect('cierres_caja:detalle_cierre', cierre_id=cierre.id)
    else:
        form = CerrarCajaForm(instance=cierre)
    
    return render(request, 'cierres_caja/form_cierre.html', {
        'form': form,
        'accion': 'Cerrar',
        'cierre': cierre,
        'pagos_dia': pagos_dia,
        'resumen_pagos': resumen_pagos,
        'total_sistema': total_sistema,
        'formas_pago': formas_pago
    })

@login_required
def detalle_cierre(request, cierre_id):
    cierre = get_object_or_404(CierreCaja, id=cierre_id)
    
    # Obtener los pagos del día
    pagos_dia = cierre.pagos.filter(estado='COMPLETADO')
    
    # Calcular totales por forma de pago
    total_sistema = Decimal('0')
    
    # Agrupar pagos por forma de pago para el resumen
    resumen_pagos = pagos_dia.values('forma_pago__nombre').annotate(
        total=Sum('monto'),
        cantidad=Count('id')
    ).order_by('forma_pago__nombre')
    
    # Calcular total del sistema
    for resumen in resumen_pagos:
        total_sistema += resumen['total']
    
    return render(request, 'cierres_caja/detalle_cierre.html', {
        'cierre': cierre,
        'pagos_dia': pagos_dia,
        'resumen_pagos': resumen_pagos,
        'total_sistema': total_sistema
    })
