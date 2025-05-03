from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from .models import Tratamiento, DetalleTratamiento
from .forms import TratamientoForm, DetalleTratamientoFormSet
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
    tratamientos = Tratamiento.objects.all().order_by('-fecha_creacion')
    return render(request, 'tratamientos/lista.html', {
        'tratamientos': tratamientos,
        'estados': dict(Tratamiento.ESTADO_CHOICES)
    })

# Vista de creación
@login_required
@ensure_csrf_cookie
def crear_tratamiento(request):
    # Asegurar que el token CSRF esté disponible
    get_token(request)
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        formset = DetalleTratamientoFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el tratamiento
                    tratamiento = form.save(commit=False)
                    tratamiento.creado_por = request.user
                    tratamiento.fecha_creacion = timezone.now()
                    tratamiento.fecha_actualizacion = timezone.now()
                    
                    # Asignar el profesional del primer detalle como profesional del tratamiento
                    profesional_asignado = False
                    for detalle_form in formset:
                        if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                            if detalle_form.cleaned_data.get('profesional'):
                                tratamiento.profesional = detalle_form.cleaned_data['profesional']
                                profesional_asignado = True
                                break
                    
                    if not profesional_asignado:
                        messages.error(request, 'Debe asignar un profesional al menos en un procedimiento')
                        return render(request, 'tratamientos/form_tratamiento.html', {
                            'form': form,
                            'formset': formset,
                            'accion': 'Crear',
                            'pacientes': Paciente.objects.all().order_by('nombre', 'apellidos'),
                            'procedimientos': Procedimiento.objects.all().order_by('nombre'),
                            'profesionales': Profesional.objects.filter(activo=True, usuario__isnull=False).select_related('usuario').order_by('apellido_paterno', 'apellido_materno', 'nombres'),
                            'today': date.today()
                        })
                    
                    tratamiento.save()
                    
                    # Guardar los detalles del tratamiento
                    for detalle_form in formset:
                        if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                            detalle = detalle_form.save(commit=False)
                            detalle.tratamiento = tratamiento
                            detalle.save()
                    
                    # Actualizar el costo total del tratamiento
                    tratamiento.costo_total = tratamiento.calcular_costo_total()
                    tratamiento.save()
                    
                    messages.success(request, 'Tratamiento creado exitosamente')
                    return redirect('tratamientos:detalle_tratamiento', pk=tratamiento.pk)
            except Exception as e:
                messages.error(request, f'Error al crear el tratamiento: {str(e)}')
        else:
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                messages.error(request, f'Error en {field}: {", ".join(errors)}')
            for form in formset:
                for field, errors in form.errors.items():
                    messages.error(request, f'Error en procedimiento - {field}: {", ".join(errors)}')
    else:
        # Inicializar el formulario con datos por defecto
        initial = {
            'fecha_inicio': date.today(),
            'fecha_fin': date.today(),
            'estado': 'PENDIENTE'
        }
        form = TratamientoForm(initial=initial)
        formset = DetalleTratamientoFormSet()

    # Obtener los datos para los selects
    pacientes = Paciente.objects.all().order_by('nombre', 'apellidos')
    procedimientos = Procedimiento.objects.all().order_by('nombre')
    profesionales = Profesional.objects.filter(activo=True).select_related('usuario').order_by('apellido_paterno', 'apellido_materno', 'nombres')

    # Pasar los profesionales al formset
    for form in formset:
        form.fields['profesional'].queryset = User.objects.filter(groups__name='Profesionales').order_by('first_name', 'last_name')

    return render(request, 'tratamientos/form_tratamiento.html', {
        'form': form,
        'formset': formset,
        'accion': 'Crear',
        'pacientes': pacientes,
        'procedimientos': procedimientos,
        'profesionales': profesionales,
        'today': date.today(),
        'estados': dict(Tratamiento.ESTADO_CHOICES)
    })

@login_required
def detalle_tratamiento(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    return render(request, 'tratamientos/detalle.html', {
        'tratamiento': tratamiento
    })

@login_required
def actualizar_estado(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        tratamiento.estado = nuevo_estado
        tratamiento.save()
        messages.success(request, 'Estado del tratamiento actualizado')
    return redirect('tratamientos:detalle_tratamiento', pk=pk)

@login_required
def marcar_pagado(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        tratamiento.pagado = True
        tratamiento.save()
        messages.success(request, 'Tratamiento marcado como pagado')
    return redirect('tratamientos:detalle_tratamiento', pk=pk)

# Vista de edición
@login_required
@ensure_csrf_cookie
def editar_tratamiento(request, pk):
    # Asegurar que el token CSRF esté disponible
    get_token(request)
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        formset = DetalleTratamientoFormSet(request.POST, instance=tratamiento)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el tratamiento
                    tratamiento = form.save()
                    
                    # Guardar los detalles del tratamiento
                    for detalle_form in formset:
                        if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                            detalle = detalle_form.save(commit=False)
                            detalle.tratamiento = tratamiento
                            detalle.save()
                    
                    messages.success(request, 'Tratamiento actualizado correctamente.')
                    return redirect('tratamientos:detalle_tratamiento', pk=pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar el tratamiento: {str(e)}')
        else:
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                messages.error(request, f'Error en {field}: {", ".join(errors)}')
            for form in formset:
                for field, errors in form.errors.items():
                    messages.error(request, f'Error en procedimiento - {field}: {", ".join(errors)}')
    else:
        # Inicializar el formulario con los datos del tratamiento
        form = TratamientoForm(instance=tratamiento)
        formset = DetalleTratamientoFormSet(instance=tratamiento)

    # Obtener los datos para los selects
    pacientes = Paciente.objects.all().order_by('nombre', 'apellidos')
    procedimientos = Procedimiento.objects.all().order_by('nombre')
    profesionales = Profesional.objects.filter(activo=True).select_related('usuario').order_by('apellido_paterno', 'apellido_materno', 'nombres')

    return render(request, 'tratamientos/form_tratamiento.html', {
        'form': form,
        'formset': formset,
        'accion': 'Editar',
        'pacientes': pacientes,
        'procedimientos': procedimientos,
        'profesionales': profesionales,
        'tratamiento': tratamiento,
        'estados': dict(Tratamiento.ESTADO_CHOICES)
    })

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