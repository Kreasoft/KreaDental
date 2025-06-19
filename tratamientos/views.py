from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from .models import Tratamiento, DetalleTratamiento, Pago
from .forms import TratamientoForm, DetalleTratamientoFormSet, PagoForm
from pacientes.models import Paciente
from procedimientos.models import Procedimiento
from datetime import date
from django.utils import timezone
from profesionales.models import Profesional
from django.core import exceptions

User = get_user_model()

# Vista de lista
@login_required
def lista_tratamientos(request):
    tratamientos = Tratamiento.objects.all().order_by('-fecha_inicio')
    return render(request, 'tratamientos/lista_tratamientos.html', {
        'tratamientos': tratamientos,
        'titulo': 'Tratamientos',
        'subtitulo': 'Lista de tratamientos registrados'
    })

# Vista de creación
@login_required
@ensure_csrf_cookie
def crear_tratamiento(request):
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        formset = DetalleTratamientoFormSet(request.POST, prefix='detalles')
        
        if form.is_valid() and formset.is_valid():
            tratamiento = form.save()
            detalles = formset.save(commit=False)
            
            for detalle in detalles:
                detalle.tratamiento = tratamiento
                detalle.save()
            
            messages.success(request, 'Tratamiento creado exitosamente.')
            return redirect('tratamientos:lista')
    else:
        form = TratamientoForm()
        formset = DetalleTratamientoFormSet(prefix='detalles')
    
    context = {
        'form': form,
        'formset': formset,
        'pacientes': Paciente.objects.all().order_by('apellidos', 'nombre'),
        'profesionales': Profesional.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombres'),
        'procedimientos': Procedimiento.objects.all().order_by('nombre'),
        'titulo': 'Nuevo Tratamiento',
        'subtitulo': 'Complete los datos del nuevo tratamiento'
    }
    return render(request, 'tratamientos/form_tratamiento.html', context)

@login_required
def detalle_tratamiento(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    return render(request, 'tratamientos/detalle_tratamiento.html', {
        'tratamiento': tratamiento,
        'titulo': 'Detalle de Tratamiento',
        'subtitulo': f'Información del tratamiento de {tratamiento.paciente}'
    })

@login_required
def actualizar_estado(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Tratamiento.ESTADO_CHOICES):
            tratamiento.estado = nuevo_estado
            tratamiento.fecha_actualizacion = timezone.now()
            tratamiento.save()
            messages.success(request, f'Estado del tratamiento actualizado a {dict(Tratamiento.ESTADO_CHOICES)[nuevo_estado]}')
            return redirect('tratamientos:lista')
        else:
            messages.error(request, 'Estado inválido')
    return redirect('tratamientos:detalle', pk=pk)

@login_required
def marcar_pagado(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        tratamiento.pagado = True
        tratamiento.fecha_actualizacion = timezone.now()
        tratamiento.save(update_fields=['pagado', 'fecha_actualizacion'])
        messages.success(request, 'Tratamiento marcado como pagado exitosamente')
        return redirect('tratamientos:lista')
    return redirect('tratamientos:detalle', pk=pk)

# Vista de edición
@login_required
@ensure_csrf_cookie
def editar_tratamiento(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        formset = DetalleTratamientoFormSet(request.POST, prefix='detalles', instance=tratamiento)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    formset.save()
                messages.success(request, 'Tratamiento actualizado exitosamente.')
                return redirect('tratamientos:lista')
            except Exception as e:
                messages.error(request, f'Error al actualizar el tratamiento: {str(e)}')
    else:
        form = TratamientoForm(instance=tratamiento)
        formset = DetalleTratamientoFormSet(prefix='detalles', instance=tratamiento)
    
    context = {
        'form': form,
        'formset': formset,
        'pacientes': Paciente.objects.all().order_by('apellidos', 'nombre'),
        'profesionales': Profesional.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombres'),
        'procedimientos': Procedimiento.objects.all().order_by('nombre'),
        'titulo': 'Editar Tratamiento',
        'subtitulo': 'Modifique los datos del tratamiento',
        'tratamiento': tratamiento
    }
    return render(request, 'tratamientos/form_tratamiento.html', context)

# Vista de eliminación
@login_required
def eliminar_tratamiento(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        try:
            tratamiento.delete()
            messages.success(request, 'Tratamiento eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el tratamiento: {str(e)}')
        return redirect('tratamientos:lista_tratamientos')
    
    return render(request, 'tratamientos/confirmar_eliminar.html', {
        'tratamiento': tratamiento
    })

@login_required
def pagos_tratamiento(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    pagos = Pago.objects.filter(tratamiento=tratamiento).order_by('-fecha')
    
    context = {
        'tratamiento': tratamiento,
        'pagos': pagos,
        'titulo': 'Pagos del Tratamiento',
        'subtitulo': f'Gestione los pagos del tratamiento de {tratamiento.paciente.nombre_completo}'
    }
    return render(request, 'tratamientos/pagos_tratamiento.html', context)

@login_required
def nuevo_pago(request):
    tratamiento_id = request.GET.get('tratamiento')
    if tratamiento_id:
        tratamiento = get_object_or_404(Tratamiento, pk=tratamiento_id)
    else:
        tratamiento = None
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            if tratamiento:
                pago.tratamiento = tratamiento
            pago.save()
            messages.success(request, 'Pago registrado exitosamente.')
            return redirect('tratamientos:pagos_tratamiento', pk=pago.tratamiento.id)
    else:
        form = PagoForm(initial={'tratamiento': tratamiento})
    
    context = {
        'form': form,
        'tratamiento': tratamiento,
        'titulo': 'Nuevo Pago',
        'subtitulo': 'Registre un nuevo pago'
    }
    return render(request, 'tratamientos/form_pago.html', context)

@login_required
def editar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago actualizado exitosamente.')
            return redirect('tratamientos:pagos_tratamiento', pk=pago.tratamiento.id)
    else:
        form = PagoForm(instance=pago)
    
    context = {
        'form': form,
        'pago': pago,
        'titulo': 'Editar Pago',
        'subtitulo': 'Modifique los datos del pago'
    }
    return render(request, 'tratamientos/form_pago.html', context)

@login_required
def eliminar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    tratamiento_id = pago.tratamiento.id
    
    if request.method == 'POST':
        try:
            pago.delete()
            messages.success(request, 'Pago eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el pago: {str(e)}')
        return redirect('tratamientos:pagos_tratamiento', pk=tratamiento_id)
    
    return render(request, 'tratamientos/confirmar_eliminar_pago.html', {
        'pago': pago
    }) 