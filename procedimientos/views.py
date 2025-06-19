from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from decimal import Decimal
from datetime import datetime
from .models import Procedimiento
from .forms import ProcedimientoForm

@login_required
def lista_procedimientos(request):
    procedimientos = Procedimiento.objects.all()
    return render(request, 'procedimientos/lista_procedimientos_nuevo.html', {
        'procedimientos': procedimientos,
        'now': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@login_required
def crear_procedimiento(request):
    if request.method == 'POST':
        form = ProcedimientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Procedimiento creado exitosamente')
            return redirect('procedimientos:lista_procedimientos')
    else:
        form = ProcedimientoForm()
    return render(request, 'procedimientos/form_procedimiento_nuevo.html', {
        'form': form,
        'accion': 'Crear',
        'now': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@login_required
def editar_procedimiento(request, procedimiento_id):
    procedimiento = get_object_or_404(Procedimiento, id=procedimiento_id)
    if request.method == 'POST':
        form = ProcedimientoForm(request.POST, instance=procedimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Procedimiento actualizado exitosamente')
            return redirect('procedimientos:lista_procedimientos')
    else:
        form = ProcedimientoForm(instance=procedimiento)
    return render(request, 'procedimientos/form_procedimiento_nuevo.html', {
        'form': form,
        'accion': 'Editar',
        'now': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@login_required
def eliminar_procedimiento(request, procedimiento_id):
    if not request.method == 'POST':
        return redirect('procedimientos:lista_procedimientos')
        
    try:
        procedimiento = Procedimiento.objects.get(id=procedimiento_id)
        procedimiento.delete()
        
        # Si es una petición HTMX, devolver 200 OK
        if request.headers.get('HX-Request'):
            return HttpResponse(status=200)
            
        messages.success(request, 'Procedimiento eliminado exitosamente')
        return redirect('procedimientos:lista_procedimientos')
        
    except Procedimiento.DoesNotExist:
        if request.headers.get('HX-Request'):
            return HttpResponse('El procedimiento no existe', status=404)
        messages.error(request, 'El procedimiento no existe')
        
    except Exception as e:
        if request.headers.get('HX-Request'):
            return HttpResponse(f'Error al eliminar el procedimiento: {str(e)}', status=500)
        messages.error(request, f'Error al eliminar el procedimiento: {str(e)}')
    
    return redirect('procedimientos:lista_procedimientos')

@login_required
def test_template(request):
    """Vista de prueba para verificar templates"""
    return render(request, 'procedimientos/test_template.html', {
        'now': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })