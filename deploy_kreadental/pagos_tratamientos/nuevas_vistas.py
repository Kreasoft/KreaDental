from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PagoAtencion
from formas_pago.models import FormaPago

@login_required
def editar_pago_atencion(request, pago_id):
    """Editar pago de atención"""
    pago = get_object_or_404(PagoAtencion, id=pago_id)
    formas_pago = FormaPago.objects.filter(estado=True)
    
    if request.method == 'POST':
        try:
            monto_str = request.POST.get('monto', '').strip()
            forma_pago_id = request.POST.get('forma_pago')
            tipo_pago = request.POST.get('tipo_pago')
            comprobante = request.POST.get('comprobante', '')
            notas = request.POST.get('notas', '')
            
            # Validar datos requeridos
            if not monto_str or not forma_pago_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Monto y forma de pago son obligatorios'
                })
            
            # Limpiar y validar monto
            monto_str = monto_str.replace(' ', '').replace(',', '.')
            if not monto_str.replace('.', '').replace('-', '').isdigit():
                return JsonResponse({
                    'status': 'error',
                    'message': 'El monto debe ser un número válido'
                })
            
            monto = float(monto_str)
            if monto <= 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El monto debe ser mayor a 0'
                })
            
            # Obtener forma de pago
            forma_pago = get_object_or_404(FormaPago, id=forma_pago_id)
            
            # Actualizar el pago
            pago.monto = monto
            pago.forma_pago = forma_pago
            pago.tipo_pago = tipo_pago
            pago.comprobante = comprobante
            pago.notas = notas
            pago.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Pago de atención actualizado exitosamente',
                'pago_id': pago.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error al actualizar el pago: {str(e)}'
            })
    
    # GET request - mostrar formulario
    context = {
        'pago': pago,
        'formas_pago': formas_pago
    }
    
    return render(request, 'pagos_tratamientos/editar_pago_atencion.html', context)

@login_required
def anular_pago_atencion(request, pago_id):
    """Anular pago de atención"""
    pago = get_object_or_404(PagoAtencion, id=pago_id)
    
    if request.method == 'POST':
        try:
            motivo = request.POST.get('motivo', '')
            
            # Anular el pago
            pago.estado = 'ANULADO'
            pago.notas = f"{pago.notas}\n\nANULADO: {motivo}".strip()
            pago.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Pago de atención anulado exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error al anular el pago: {str(e)}'
            })
    
    # GET request - mostrar confirmación
    context = {
        'pago': pago
    }
    
    return render(request, 'pagos_tratamientos/anular_pago_atencion.html', context)





