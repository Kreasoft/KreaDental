from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Especialidad
from .forms import EspecialidadForm

@login_required
def lista_especialidades(request):
    especialidades = Especialidad.objects.all().order_by('nombre')
    return render(request, 'especialidades/lista_especialidades.html', {
        'especialidades': especialidades
    })

@login_required
def nueva_especialidad(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            especialidad = form.save(commit=False)
            # Asegurarnos que el estado se guarde correctamente
            especialidad.estado = form.cleaned_data.get('estado', True)
            especialidad.save()
            messages.success(request, 'Especialidad creada correctamente.')
            return redirect('especialidades:lista_especialidades')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = EspecialidadForm()
    
    return render(request, 'especialidades/form_especialidad.html', {
        'form': form,
        'accion': 'Nueva'
    })

@login_required
def editar_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            especialidad = form.save(commit=False)
            # Asegurarnos que el estado se guarde correctamente
            especialidad.estado = form.cleaned_data.get('estado', True)
            especialidad.save()
            messages.success(request, 'Especialidad actualizada correctamente.')
            return redirect('especialidades:lista_especialidades')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = EspecialidadForm(instance=especialidad)
    
    return render(request, 'especialidades/form_especialidad.html', {
        'form': form,
        'especialidad': especialidad,
        'accion': 'Editar'
    })

@login_required
def eliminar_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        try:
            especialidad.delete()
            return redirect('especialidades:lista_especialidades')
        except:
            return render(request, 'especialidades/confirmar_eliminar.html', {
                'especialidad': especialidad,
                'error': 'No se puede eliminar esta especialidad porque está siendo utilizada.'
            })
    
    return render(request, 'especialidades/confirmar_eliminar.html', {
        'especialidad': especialidad
    })

def especialidad_create(request):
    data = dict()
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            especialidades = Especialidad.objects.all()
            data['html_especialidad_list'] = render_to_string(
                'especialidades/includes/partial_especialidad_list.html',
                {'especialidades': especialidades}
            )
        else:
            data['form_is_valid'] = False
    else:
        form = EspecialidadForm()
    
    context = {'form': form}
    data['html_form'] = render_to_string(
        'especialidades/includes/partial_especialidad_create.html',
        context,
        request=request
    )
    return JsonResponse(data)

def especialidad_update(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    data = dict()
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            especialidades = Especialidad.objects.all()
            data['html_especialidad_list'] = render_to_string(
                'especialidades/includes/partial_especialidad_list.html',
                {'especialidades': especialidades}
            )
        else:
            data['form_is_valid'] = False
    else:
        form = EspecialidadForm(instance=especialidad)
    
    context = {'form': form, 'especialidad': especialidad}
    data['html_form'] = render_to_string(
        'especialidades/includes/partial_especialidad_update.html',
        context,
        request=request
    )
    return JsonResponse(data)

def especialidad_delete(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    data = dict()
    if request.method == 'POST':
        especialidad.delete()
        data['form_is_valid'] = True
        especialidades = Especialidad.objects.all()
        data['html_especialidad_list'] = render_to_string(
            'especialidades/includes/partial_especialidad_list.html',
            {'especialidades': especialidades}
        )
    else:
        context = {'especialidad': especialidad}
        data['html_form'] = render_to_string(
            'especialidades/includes/partial_especialidad_delete.html',
            context,
            request=request
        )
    return JsonResponse(data) 