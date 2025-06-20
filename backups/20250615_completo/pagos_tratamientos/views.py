from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from .models import PagoTratamiento, HistorialPago
from tratamientos.models import Tratamiento
from formas_pago.models import FormaPago

@login_required
def lista_pagos(request):
    pagos = PagoTratamiento.objects.all().order_by('-fecha_pago')
    
    # Filtrar por tratamiento si se proporciona el ID
    tratamiento_id = request.GET.get('tratamiento')
    if tratamiento_id:
        pagos = pagos.filter(tratamiento_id=tratamiento_id)
        tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)
    else:
        tratamiento = None
    
    # Estadísticas
    total_pagos = pagos.filter(estado='COMPLETADO').aggregate(total=Sum('monto'))['total'] or 0
    pagos_pendientes = pagos.filter(estado='PENDIENTE').count()
    pagos_completados = pagos.filter(estado='COMPLETADO').count()
    pagos_anulados = pagos.filter(estado='ANULADO').count()
    
    context = {
        'pagos': pagos,
        'total_pagos': total_pagos,
        'pagos_pendientes': pagos_pendientes,
        'pagos_completados': pagos_completados,
        'pagos_anulados': pagos_anulados,
        'tratamiento': tratamiento
    }
    
    return render(request, 'pagos_tratamientos/lista_pagos.html', context)

@login_required
def crear_pago(request, tratamiento_id):
    tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)
    formas_pago = FormaPago.objects.filter(estado=True)
    
    if request.method == 'POST':
        try:
            monto = float(request.POST.get('monto'))
            forma_pago_id = request.POST.get('forma_pago')
            comprobante = request.POST.get('comprobante', '')
            notas = request.POST.get('notas', '')
            
            forma_pago = get_object_or_404(FormaPago, id=forma_pago_id)
            
            pago = PagoTratamiento.objects.create(
                tratamiento=tratamiento,
                forma_pago=forma_pago,
                monto=monto,
                comprobante=comprobante,
                notas=notas,
                creado_por=request.user,
                estado='COMPLETADO'
            )
            
            # Crear registro en el historial
            HistorialPago.objects.create(
                pago=pago,
                tipo_accion='CREACION',
                estado_nuevo='COMPLETADO',
                monto_nuevo=monto,
                realizado_por=request.user
            )
            
            messages.success(request, 'Pago registrado exitosamente.')
            return redirect('detalle_tratamiento', tratamiento_id=tratamiento.id)
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Error al procesar el pago.')
    
    # Calcular saldo pendiente
    pagos_completados = tratamiento.pagos.filter(estado='COMPLETADO')
    total_pagado = pagos_completados.aggregate(total=Sum('monto'))['total'] or 0
    saldo_pendiente = tratamiento.costo_total - total_pagado
    
    context = {
        'tratamiento': tratamiento,
        'formas_pago': formas_pago,
        'saldo_pendiente': saldo_pendiente
    }
    
    return render(request, 'pagos_tratamientos/crear_pago.html', context)

@login_required
def anular_pago(request, pago_id):
    if request.method == 'POST':
        pago = get_object_or_404(PagoTratamiento, id=pago_id)
        
        if pago.estado == 'ANULADO':
            return JsonResponse({
                'status': 'error',
                'message': 'Este pago ya está anulado.'
            })
        
        try:
            estado_anterior = pago.estado
            monto_anterior = pago.monto
            
            pago.estado = 'ANULADO'
            pago.save()
            
            # Crear registro en el historial
            HistorialPago.objects.create(
                pago=pago,
                tipo_accion='ANULACION',
                estado_anterior=estado_anterior,
                estado_nuevo='ANULADO',
                monto_anterior=monto_anterior,
                monto_nuevo=pago.monto,
                realizado_por=request.user,
                notas=request.POST.get('motivo_anulacion', '')
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Pago anulado exitosamente.'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error al anular el pago: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido.'
    })

@login_required
def detalle_pago(request, pago_id):
    pago = get_object_or_404(PagoTratamiento, id=pago_id)
    historial = pago.historial.all().order_by('-fecha_accion')
    
    context = {
        'pago': pago,
        'historial': historial
    }
    
    return render(request, 'pagos_tratamientos/detalle_pago.html', context)

@login_required
def editar_pago(request, pago_id):
    pago = get_object_or_404(PagoTratamiento, id=pago_id)
    formas_pago = FormaPago.objects.filter(estado=True)
    
    if request.method == 'POST':
        try:
            monto = float(request.POST.get('monto'))
            forma_pago_id = request.POST.get('forma_pago')
            comprobante = request.POST.get('comprobante', '')
            notas = request.POST.get('notas', '')
            
            forma_pago = get_object_or_404(FormaPago, id=forma_pago_id)
            
            # Guardar valores anteriores para el historial
            estado_anterior = pago.estado
            monto_anterior = pago.monto
            forma_pago_anterior = pago.forma_pago
            
            # Actualizar el pago
            pago.forma_pago = forma_pago
            pago.monto = monto
            pago.comprobante = comprobante
            pago.notas = notas
            pago.save()
            
            # Crear registro en el historial
            HistorialPago.objects.create(
                pago=pago,
                tipo_accion='MODIFICACION',
                estado_anterior=estado_anterior,
                estado_nuevo=pago.estado,
                monto_anterior=monto_anterior,
                monto_nuevo=monto,
                realizado_por=request.user,
                notas=f'Forma de pago anterior: {forma_pago_anterior}, Nueva forma de pago: {forma_pago}'
            )
            
            messages.success(request, 'Pago actualizado exitosamente.')
            return redirect('pagos_tratamientos:detalle_pago', pago_id=pago.id)
            
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Error al actualizar el pago.')
    
    context = {
        'pago': pago,
        'formas_pago': formas_pago,
        'tratamiento': pago.tratamiento
    }
    
    return render(request, 'pagos_tratamientos/editar_pago.html', context)
