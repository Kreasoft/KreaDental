from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Profesional, Especialidad
from .forms import ProfesionalForm, EspecialidadForm
from usuarios.models import Usuario
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
import re
from django.db.models import Count
from empresa.utils import get_empresa_actual
from citas.models import Cita

@login_required
def lista_profesionales(request):
    # Obtener la empresa actual del usuario
    empresa_actual = get_empresa_actual(request)
    
    # Obtener todos los profesionales de la empresa actual
    profesionales = Profesional.objects.filter(empresa=empresa_actual).select_related('especialidad')
    
    # Estadísticas
    total_profesionales = profesionales.count()
    profesionales_activos = profesionales.filter(activo=True).count()
    profesionales_por_especialidad = profesionales.values('especialidad__nombre').annotate(total=Count('id'))
    citas_mes = Cita.objects.filter(
        profesional__in=profesionales,
        fecha__month=timezone.now().month,
        fecha__year=timezone.now().year
    ).count()
    
    # Obtener todas las especialidades
    especialidades = Especialidad.objects.all()
    
    context = {
        'profesionales': profesionales,
        'total_profesionales': total_profesionales,
        'profesionales_activos': profesionales_activos,
        'profesionales_por_especialidad': dict(profesionales_por_especialidad.values_list('especialidad__nombre', 'total')),
        'citas_mes': citas_mes,
        'especialidades': especialidades,
        'empresa_actual': empresa_actual,
    }
    
    return render(request, 'profesionales/lista_profesionales.html', context)

@login_required
def nuevo_profesional(request):
    if request.method == 'POST':
        form = ProfesionalForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    profesional = form.save(commit=False)
                    profesional.empresa = get_empresa_actual(request)
                    profesional.save()
                    messages.success(request, 'Profesional agregado exitosamente.')
                    return redirect('profesionales:lista_profesionales')
            except Exception as e:
                messages.error(request, f'Error al crear el profesional: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProfesionalForm()
    
    especialidades = Especialidad.objects.all()
    context = {
        'form': form,
        'accion': 'Nuevo',
        'especialidades': especialidades,
        'empresa_actual': get_empresa_actual(request),
    }
    return render(request, 'profesionales/form_profesional.html', context)

@login_required
def editar_profesional(request, pk):
    profesional = get_object_or_404(Profesional, id=pk)
    
    if request.method == 'POST':
        form = ProfesionalForm(request.POST, instance=profesional)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profesional actualizado exitosamente.')
            return redirect('profesionales:lista_profesionales')
    else:
        form = ProfesionalForm(instance=profesional)
    
    especialidades = Especialidad.objects.all()
    context = {
        'form': form,
        'accion': 'Editar',
        'especialidades': especialidades,
        'empresa_actual': get_empresa_actual(request),  # Agregar empresa actual al contexto
    }
    return render(request, 'profesionales/form_profesional.html', context)

@login_required
def eliminar_profesional(request, pk):
    profesional = get_object_or_404(Profesional, pk=pk)
    if request.method == 'POST':
        if profesional.usuario:  # Verificar si tiene usuario asociado
            profesional.usuario.delete()  # Eliminar el usuario asociado
        profesional.delete()  # Eliminar el profesional
        messages.success(request, 'Profesional eliminado exitosamente.')
        return redirect('profesionales:lista_profesionales')
    return render(request, 'profesionales/confirmar_eliminar.html', {'profesional': profesional})

@login_required
def lista_especialidades(request):
    especialidades = Especialidad.objects.all().order_by('nombre')
    especialidades_activas = especialidades.filter(estado=True).count()
    especialidades_inactivas = especialidades.filter(estado=False).count()
    return render(request, 'profesionales/especialidades/lista_especialidades.html', {
        'especialidades': especialidades,
        'especialidades_activas': especialidades_activas,
        'especialidades_inactivas': especialidades_inactivas
    })

@login_required
def crear_especialidad(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            especialidad = form.save(commit=False)
            especialidad.estado = form.cleaned_data.get('estado', True)
            especialidad.save()
            messages.success(request, 'Especialidad creada exitosamente.')
            return redirect('profesionales:lista_especialidades')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EspecialidadForm()
    
    context = {
        'form': form,
        'accion': 'Crear'
    }
    return render(request, 'profesionales/especialidades/crear_especialidad.html', context)

@login_required
def editar_especialidad(request, especialidad_id):
    especialidad = get_object_or_404(Especialidad, id=especialidad_id)
    
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad actualizada exitosamente.')
            return redirect('profesionales:lista_especialidades')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EspecialidadForm(instance=especialidad)
    
    context = {
        'form': form,
        'especialidad': especialidad,
        'accion': 'Editar'
    }
    return render(request, 'profesionales/especialidades/editar_especialidad.html', context)

@login_required
def eliminar_especialidad(request, especialidad_id):
    especialidad = get_object_or_404(Especialidad, id=especialidad_id)
    
    if request.method == 'POST':
        nombre = especialidad.nombre
        especialidad.delete()
        messages.success(request, f'Especialidad "{nombre}" eliminada exitosamente.')
        return redirect('profesionales:lista_especialidades')
    
    context = {
        'especialidad': especialidad
    }
    return render(request, 'profesionales/especialidades/confirmar_eliminar_especialidad.html', context)

@login_required
def obtener_profesionales(request):
    """Vista para obtener todos los profesionales de la empresa actual"""
    empresa_actual = get_empresa_actual(request)
    
    profesionales = Profesional.objects.filter(
        empresa=empresa_actual,
        activo=True
    ).select_related('especialidad')
    
    results = []
    for profesional in profesionales:
        results.append({
            'id': profesional.id,
            'nombres': profesional.nombres,
            'apellido_paterno': profesional.apellido_paterno,
            'apellido_materno': profesional.apellido_materno,
            'especialidad': profesional.especialidad.nombre if profesional.especialidad else 'Sin especialidad'
        })
    
    return JsonResponse({'results': results})

@login_required
def buscar_profesionales(request):
    """Vista para búsqueda AJAX de profesionales"""
    query = request.GET.get('q', '')
    empresa_actual = get_empresa_actual(request)
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    # Buscar profesionales por nombres, apellidos o especialidad
    profesionales = Profesional.objects.filter(
        Q(empresa=empresa_actual) &
        Q(activo=True) &
        (Q(nombres__icontains=query) | 
         Q(apellido_paterno__icontains=query) |
         Q(apellido_materno__icontains=query) |
         Q(especialidad__nombre__icontains=query))
    ).select_related('especialidad')[:10]
    
    results = []
    for profesional in profesionales:
        results.append({
            'id': profesional.id,
            'nombres': profesional.nombres,
            'apellido_paterno': profesional.apellido_paterno,
            'apellido_materno': profesional.apellido_materno,
            'especialidad': profesional.especialidad.nombre if profesional.especialidad else 'Sin especialidad'
        })
    
    return JsonResponse({'results': results}) 