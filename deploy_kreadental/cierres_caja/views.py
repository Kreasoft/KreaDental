from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models
from django.db.models import Sum, Count
from django.conf import settings
from django.http import HttpResponse
# Removido Decimal ya que ahora usamos enteros
from datetime import timedelta
from .models import CierreCaja, RetiroCaja
from .forms import CierreCajaForm, CerrarCajaForm, RetiroCajaForm
from pagos_tratamientos.models import PagoTratamiento, PagoAtencion
from tratamientos.models import Pago
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
    total_efectivo = cierres.aggregate(total=Sum('total_efectivo'))['total'] or 0
    total_tarjeta = cierres.aggregate(total=Sum('total_tarjeta'))['total'] or 0
    total_transferencia = cierres.aggregate(total=Sum('total_transferencia'))['total'] or 0
    total_ingresos = total_efectivo + total_tarjeta + total_transferencia
    
    total_egresos = 0  # Por ahora no hay egresos en el modelo
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
    # Verificar si ya hay una caja abierta HOY
    hoy = timezone.now().date()
    caja_abierta_hoy = CierreCaja.objects.filter(
        estado='ABIERTO',
        fecha=hoy
    ).first()
    
    if caja_abierta_hoy:
        messages.error(request, f'Ya hay una caja abierta para el día {hoy.strftime("%d/%m/%Y")}. Debe cerrar la caja actual antes de abrir una nueva.')
        return redirect('cierres_caja:lista_cierres')
    
    # Verificar si ya se abrió caja hoy (aunque esté cerrada)
    caja_hoy = CierreCaja.objects.filter(fecha=hoy).first()
    if caja_hoy:
        messages.error(request, f'Ya se abrió y cerró caja para el día {hoy.strftime("%d/%m/%Y")}. Solo se puede abrir una caja por día.')
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
    
    # Obtener todos los tipos de pagos del día
    # 1. Pagos de Tratamientos
    pagos_tratamientos = PagoTratamiento.objects.filter(
        fecha_pago__date=cierre.fecha,
        estado='COMPLETADO'
    ).select_related('forma_pago', 'tratamiento__paciente')
    
    # 2. Pagos de Atenciones
    pagos_atenciones = PagoAtencion.objects.filter(
        fecha_pago__date=cierre.fecha,
        estado='COMPLETADO'
    ).select_related('forma_pago', 'cita__paciente')
    
    # 3. Pagos Rápidos (modelo Pago)
    pagos_rapidos = Pago.objects.filter(
        fecha=cierre.fecha,
        estado='PAGADO'
    ).select_related('tratamiento__paciente')
    
    # Combinar todos los pagos para el contexto
    pagos_dia = list(pagos_tratamientos) + list(pagos_atenciones) + list(pagos_rapidos)
    
    # Calcular totales por forma de pago
    totales_por_forma = {}
    total_sistema = 0
    
    # Procesar pagos de tratamientos
    for forma in formas_pago:
        total_tratamientos = pagos_tratamientos.filter(forma_pago=forma).aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        # Procesar pagos de atenciones
        total_atenciones = pagos_atenciones.filter(forma_pago=forma).aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        # Procesar pagos rápidos (convertir metodo_pago a forma_pago)
        metodo_to_forma = {
            'EFECTIVO': 'EFECTIVO',
            'TARJETA': 'TARJETA', 
            'TRANSFERENCIA': 'TRANSFERENCIA'
        }
        forma_rapida = metodo_to_forma.get(forma.nombre, None)
        total_rapidos = 0
        if forma_rapida:
            total_rapidos = pagos_rapidos.filter(metodo_pago=forma_rapida).aggregate(
                total=Sum('monto')
            )['total'] or 0
        
        total_forma = total_tratamientos + total_atenciones + total_rapidos
        totales_por_forma[forma.nombre] = total_forma
        total_sistema += total_forma
    
    # Crear resumen de pagos combinado
    resumen_pagos = []
    for forma in formas_pago:
        cantidad_tratamientos = pagos_tratamientos.filter(forma_pago=forma).count()
        cantidad_atenciones = pagos_atenciones.filter(forma_pago=forma).count()
        
        # Contar pagos rápidos
        metodo_to_forma = {
            'EFECTIVO': 'EFECTIVO',
            'TARJETA': 'TARJETA', 
            'TRANSFERENCIA': 'TRANSFERENCIA'
        }
        forma_rapida = metodo_to_forma.get(forma.nombre, None)
        cantidad_rapidos = 0
        if forma_rapida:
            cantidad_rapidos = pagos_rapidos.filter(metodo_pago=forma_rapida).count()
        
        total_cantidad = cantidad_tratamientos + cantidad_atenciones + cantidad_rapidos
        total_monto = totales_por_forma[forma.nombre]
        
        if total_cantidad > 0:  # Solo incluir formas de pago con pagos
            resumen_pagos.append({
                'forma_pago__nombre': forma.nombre,
                'cantidad': total_cantidad,
                'total': total_monto
            })
    
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
                print(f"DEBUG CIERRE: monto_final={cierre.monto_final}, monto_inicial={cierre.monto_inicial}, total_sistema={total_sistema}, diferencia={cierre.diferencia}")
            else:
                cierre.diferencia = 0  # Establecer un valor por defecto
                print(f"DEBUG CIERRE: monto_final es None, diferencia=0")
            
            # Actualizar estado y usuario
            cierre.estado = 'CERRADO'
            cierre.usuario_cierre = request.user
            cierre.hora_cierre = timezone.now().time()
            
            # Guardar cierre
            cierre.save()
            
            messages.success(request, 'Caja cerrada exitosamente')
            return redirect('cierres_caja:detalle_cierre', cierre_id=cierre.id)
    else:
        form = CerrarCajaForm(instance=cierre)
    
    return render(request, 'cierres_caja/form_cierre.html', {
        'form': form,
        'accion': 'Cerrar',
        'cierre': cierre,
        'pagos_dia': pagos_dia,
        'pagos_tratamientos': pagos_tratamientos,
        'pagos_atenciones': pagos_atenciones,
        'pagos_rapidos': pagos_rapidos,
        'resumen_pagos': resumen_pagos,
        'total_sistema': total_sistema,
        'formas_pago': formas_pago
    })

@login_required
def detalle_cierre(request, cierre_id):
    cierre = get_object_or_404(CierreCaja, id=cierre_id)
    
    # Obtener todos los tipos de pagos del día
    # 1. Pagos de Tratamientos
    pagos_tratamientos = PagoTratamiento.objects.filter(
        fecha_pago__date=cierre.fecha,
        estado='COMPLETADO'
    ).select_related('forma_pago', 'tratamiento__paciente')
    
    # 2. Pagos de Atenciones
    pagos_atenciones = PagoAtencion.objects.filter(
        fecha_pago__date=cierre.fecha,
        estado='COMPLETADO'
    ).select_related('forma_pago', 'cita__paciente')
    
    # 3. Pagos Rápidos (modelo Pago)
    pagos_rapidos = Pago.objects.filter(
        fecha=cierre.fecha,
        estado='PAGADO'
    ).select_related('tratamiento__paciente')
    
    # Combinar todos los pagos
    pagos_dia = list(pagos_tratamientos) + list(pagos_atenciones) + list(pagos_rapidos)
    
    # Obtener formas de pago activas
    formas_pago = FormaPago.objects.filter(estado=True)
    
    # Calcular totales por forma de pago
    totales_por_forma = {}
    total_sistema = 0
    
    # Procesar pagos de tratamientos
    for forma in formas_pago:
        total_tratamientos = pagos_tratamientos.filter(forma_pago=forma).aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        # Procesar pagos de atenciones
        total_atenciones = pagos_atenciones.filter(forma_pago=forma).aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        # Procesar pagos rápidos (convertir metodo_pago a forma_pago)
        metodo_to_forma = {
            'EFECTIVO': 'EFECTIVO',
            'TARJETA': 'TARJETA', 
            'TRANSFERENCIA': 'TRANSFERENCIA'
        }
        forma_rapida = metodo_to_forma.get(forma.nombre, None)
        total_rapidos = 0
        if forma_rapida:
            total_rapidos = pagos_rapidos.filter(metodo_pago=forma_rapida).aggregate(
                total=Sum('monto')
            )['total'] or 0
        
        total_forma = total_tratamientos + total_atenciones + total_rapidos
        totales_por_forma[forma.nombre] = total_forma
        total_sistema += total_forma
    
    # Crear resumen de pagos combinado
    resumen_pagos = []
    for forma in formas_pago:
        cantidad_tratamientos = pagos_tratamientos.filter(forma_pago=forma).count()
        cantidad_atenciones = pagos_atenciones.filter(forma_pago=forma).count()
        
        # Contar pagos rápidos
        metodo_to_forma = {
            'EFECTIVO': 'EFECTIVO',
            'TARJETA': 'TARJETA', 
            'TRANSFERENCIA': 'TRANSFERENCIA'
        }
        forma_rapida = metodo_to_forma.get(forma.nombre, None)
        cantidad_rapidos = 0
        if forma_rapida:
            cantidad_rapidos = pagos_rapidos.filter(metodo_pago=forma_rapida).count()
        
        total_cantidad = cantidad_tratamientos + cantidad_atenciones + cantidad_rapidos
        total_monto = totales_por_forma[forma.nombre]
        
        if total_cantidad > 0:  # Solo incluir formas de pago con pagos
            resumen_pagos.append({
                'forma_pago__nombre': forma.nombre,
                'cantidad': total_cantidad,
                'total': total_monto
            })
    
    # Actualizar los totales en el modelo siempre
    cierre.total_efectivo = totales_por_forma.get('EFECTIVO', 0)
    cierre.total_tarjeta = totales_por_forma.get('TARJETA CREDITO', 0) + totales_por_forma.get('TARJETA DEBITO', 0)
    cierre.total_transferencia = totales_por_forma.get('TRANSFERENCIA', 0)
    cierre.save()
    
    return render(request, 'cierres_caja/detalle_cierre.html', {
        'cierre': cierre,
        'pagos_dia': pagos_dia,
        'pagos_tratamientos': pagos_tratamientos,
        'pagos_atenciones': pagos_atenciones,
        'pagos_rapidos': pagos_rapidos,
        'resumen_pagos': resumen_pagos,
        'total_sistema': total_sistema
    })

@login_required
def imprimir_cierre(request, cierre_id):
    """
    Vista para imprimir el cierre de caja según el tipo de impresora configurado
    """
    cierre = get_object_or_404(CierreCaja, id=cierre_id)
    
    # Obtener datos del cierre (reutilizar lógica de detalle_cierre)
    pagos_tratamientos = PagoTratamiento.objects.filter(
        fecha_pago__date=cierre.fecha,
        estado='COMPLETADO'
    ).select_related('forma_pago', 'tratamiento__paciente')
    
    pagos_atenciones = PagoAtencion.objects.filter(
        fecha_pago__date=cierre.fecha,
        estado='COMPLETADO'
    ).select_related('forma_pago', 'cita__paciente')
    
    pagos_rapidos = Pago.objects.filter(
        fecha=cierre.fecha,
        estado='PAGADO'
    ).select_related('tratamiento__paciente')
    
    # Calcular totales
    total_efectivo = sum(p.monto for p in pagos_tratamientos.filter(forma_pago__nombre__icontains='efectivo')) + \
                    sum(p.monto for p in pagos_atenciones.filter(forma_pago__nombre__icontains='efectivo')) + \
                    sum(p.monto for p in pagos_rapidos.filter(metodo_pago__icontains='efectivo'))
    
    total_tarjeta = sum(p.monto for p in pagos_tratamientos.filter(forma_pago__nombre__icontains='tarjeta')) + \
                   sum(p.monto for p in pagos_atenciones.filter(forma_pago__nombre__icontains='tarjeta')) + \
                   sum(p.monto for p in pagos_rapidos.filter(metodo_pago__icontains='tarjeta'))
    
    total_transferencia = sum(p.monto for p in pagos_tratamientos.filter(forma_pago__nombre__icontains='transferencia')) + \
                         sum(p.monto for p in pagos_atenciones.filter(forma_pago__nombre__icontains='transferencia')) + \
                         sum(p.monto for p in pagos_rapidos.filter(metodo_pago__icontains='transferencia'))
    
    total_sistema = total_efectivo + total_tarjeta + total_transferencia
    
    # Determinar tipo de impresora
    printer_type = getattr(settings, 'PRINTER_TYPE', 'THERMAL')
    
    if printer_type == 'THERMAL':
        return render(request, 'cierres_caja/print_thermal.html', {
            'cierre': cierre,
            'pagos_tratamientos': pagos_tratamientos,
            'pagos_atenciones': pagos_atenciones,
            'pagos_rapidos': pagos_rapidos,
            'total_sistema': total_sistema,
            'total_efectivo': total_efectivo,
            'total_tarjeta': total_tarjeta,
            'total_transferencia': total_transferencia,
            'printer_width': getattr(settings, 'THERMAL_PRINTER_WIDTH', 80)
        })
    else:
        return render(request, 'cierres_caja/print_laser.html', {
            'cierre': cierre,
            'pagos_tratamientos': pagos_tratamientos,
            'pagos_atenciones': pagos_atenciones,
            'pagos_rapidos': pagos_rapidos,
            'total_sistema': total_sistema,
            'total_efectivo': total_efectivo,
            'total_tarjeta': total_tarjeta,
            'total_transferencia': total_transferencia
        })


@login_required
def registrar_retiro(request, cierre_id):
    """Vista para registrar un retiro de caja"""
    cierre = get_object_or_404(CierreCaja, id=cierre_id)
    
    # Verificar que la caja esté abierta
    if cierre.estado != 'ABIERTO':
        messages.error(request, 'Solo se pueden registrar retiros en cajas abiertas.')
        return redirect('cierres_caja:detalle_cierre', cierre_id=cierre.id)
    
    if request.method == 'POST':
        monto = request.POST.get('monto', '').replace('.', '').replace(',', '').replace(' ', '')
        concepto = request.POST.get('concepto', '')
        comprobante = request.POST.get('comprobante', '')
        observaciones = request.POST.get('observaciones', '')
        
        if monto and concepto:
            try:
                monto_int = int(monto)
                retiro = RetiroCaja.objects.create(
                    cierre_caja=cierre,
                    monto=monto_int,
                    concepto=concepto,
                    comprobante=comprobante,
                    observaciones=observaciones,
                    usuario_retiro=request.user
                )
                messages.success(request, f'Retiro de ${monto_int:,} registrado exitosamente.')
                return redirect('cierres_caja:detalle_cierre', cierre_id=cierre.id)
            except ValueError:
                messages.error(request, 'El monto debe ser un número válido.')
        else:
            messages.error(request, 'El monto y concepto son requeridos.')
    
    form = RetiroCajaForm()
    
    return render(request, 'cierres_caja/registrar_retiro_simple.html', {
        'form': form,
        'cierre': cierre
    })


@login_required
def lista_retiros(request, cierre_id):
    """Vista para listar retiros de una caja específica"""
    cierre = get_object_or_404(CierreCaja, id=cierre_id)
    retiros = cierre.retiros.all().order_by('-fecha_retiro')
    
    return render(request, 'cierres_caja/lista_retiros.html', {
        'cierre': cierre,
        'retiros': retiros
    })


@login_required
def eliminar_retiro(request, retiro_id):
    """Vista para eliminar un retiro"""
    retiro = get_object_or_404(RetiroCaja, id=retiro_id)
    cierre = retiro.cierre_caja
    
    # Verificar que la caja esté abierta
    if cierre.estado != 'ABIERTO':
        messages.error(request, 'Solo se pueden eliminar retiros de cajas abiertas.')
        return redirect('cierres_caja:detalle_cierre', cierre_id=cierre.id)
    
    if request.method == 'POST':
        concepto = retiro.concepto
        monto = retiro.monto
        retiro.delete()
        
        messages.success(request, f'Retiro "{concepto}" por ${monto:,} eliminado exitosamente.')
        return redirect('cierres_caja:detalle_cierre', cierre_id=cierre.id)
    
    return render(request, 'cierres_caja/confirmar_eliminar_retiro.html', {
        'retiro': retiro
    })
