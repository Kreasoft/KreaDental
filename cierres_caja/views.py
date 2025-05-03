from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models
from decimal import Decimal
from .models import CierreCaja
from .forms import CierreCajaForm, CerrarCajaForm
from pagos_tratamientos.models import PagoTratamiento

@login_required
def lista_cierres(request):
    cierres = CierreCaja.objects.all().order_by('-fecha', '-hora_apertura')
    hay_caja_abierta = CierreCaja.objects.filter(estado='ABIERTO').exists()
    return render(request, 'cierres_caja/lista_cierres.html', {
        'cierres': cierres,
        'hay_caja_abierta': hay_caja_abierta
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
    
    if request.method == 'POST':
        form = CerrarCajaForm(request.POST, instance=cierre)
        if form.is_valid():
            cierre = form.save(commit=False)
            
            # Obtener los pagos del día
            pagos_dia = PagoTratamiento.objects.filter(
                fecha_pago__date=cierre.fecha,
                estado='COMPLETADO'
            )
            
            # Calcular totales por método de pago
            cierre.total_efectivo = pagos_dia.filter(forma_pago__nombre='EFECTIVO').aggregate(
                total=models.Sum('monto')
            )['total'] or Decimal('0')
            
            cierre.total_tarjeta = pagos_dia.filter(forma_pago__nombre='TARJETA').aggregate(
                total=models.Sum('monto')
            )['total'] or Decimal('0')
            
            cierre.total_transferencia = pagos_dia.filter(forma_pago__nombre='TRANSFERENCIA').aggregate(
                total=models.Sum('monto')
            )['total'] or Decimal('0')
            
            # Calcular diferencia
            total_sistema = cierre.total_efectivo + cierre.total_tarjeta + cierre.total_transferencia
            cierre.diferencia = cierre.monto_final - (cierre.monto_inicial + total_sistema)
            
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
        'cierre': cierre
    })

@login_required
def detalle_cierre(request, cierre_id):
    cierre = get_object_or_404(CierreCaja, id=cierre_id)
    return render(request, 'cierres_caja/detalle_cierre.html', {
        'cierre': cierre
    })
