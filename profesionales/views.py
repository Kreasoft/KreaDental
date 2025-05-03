from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Profesional
from especialidades.models import Especialidad
from .forms import ProfesionalForm, UserForm, EspecialidadForm
from django.contrib.auth.models import User

@login_required
def lista_profesionales(request):
    # Obtener todos los profesionales ordenados
    profesionales = Profesional.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombres')
    
    # Estadísticas
    total_profesionales = profesionales.count()
    profesionales_activos = profesionales.filter(activo=True).count()
    
    # Profesionales por especialidad
    especialidades = Especialidad.objects.filter(estado=True).order_by('nombre')
    profesionales_por_especialidad = {}
    for especialidad in especialidades:
        count = profesionales.filter(especialidad=especialidad, activo=True).count()
        if count > 0:
            profesionales_por_especialidad[especialidad.nombre] = count
    
    # Citas asignadas este mes
    from django.utils import timezone
    from tratamientos.models import Tratamiento
    primer_dia_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    citas_mes = Tratamiento.objects.filter(
        profesional__in=profesionales,
        fecha_inicio__gte=primer_dia_mes,
        estado='PENDIENTE'
    ).count()
    
    context = {
        'profesionales': profesionales,
        'total_profesionales': total_profesionales,
        'profesionales_activos': profesionales_activos,
        'profesionales_por_especialidad': profesionales_por_especialidad,
        'citas_mes': citas_mes,
        'especialidades': especialidades,
    }
    
    return render(request, 'profesionales/lista_profesionales.html', context)

@login_required
def nuevo_profesional(request):
    if request.method == 'POST':
        print("Iniciando proceso de creación de profesional...")
        user_form = UserForm(request.POST)
        profesional_form = ProfesionalForm(request.POST)
        
        print("Validando formularios...")
        print("User form errors:", user_form.errors if not user_form.is_valid() else "Válido")
        print("Profesional form errors:", profesional_form.errors if not profesional_form.is_valid() else "Válido")
        
        if user_form.is_valid() and profesional_form.is_valid():
            try:
                print("Guardando usuario...")
                user = user_form.save()
                print(f"Usuario creado: {user.username}")
                
                print("Guardando profesional...")
                profesional = profesional_form.save(commit=False)
                profesional.usuario = user
                profesional.save()
                print(f"Profesional creado: {profesional.nombre_completo()}")
                
                messages.success(request, 'Profesional creado exitosamente.')
                return redirect('profesionales:lista_profesionales')
            except Exception as e:
                print(f"Error al guardar: {str(e)}")
                messages.error(request, f'Error al crear el profesional: {str(e)}')
        else:
            print("Formularios inválidos")
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        print("Cargando formularios vacíos...")
        user_form = UserForm()
        profesional_form = ProfesionalForm()
        especialidades = Especialidad.objects.filter(estado=True).order_by('nombre')
        print("Especialidades disponibles:", [f"{e.id}: {e.nombre} (Estado: {e.estado})" for e in especialidades])
    
    return render(request, 'profesionales/form_profesional.html', {
        'user_form': user_form,
        'form': profesional_form,
        'accion': 'Nuevo'
    })

@login_required
def editar_profesional(request, pk):
    profesional = get_object_or_404(Profesional, pk=pk)
    if request.method == 'POST':
        form = ProfesionalForm(request.POST, instance=profesional)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profesional actualizado exitosamente.')
            return redirect('profesionales:lista_profesionales')
    else:
        form = ProfesionalForm(instance=profesional)
    
    return render(request, 'profesionales/form_profesional.html', {
        'form': form,
        'profesional': profesional,
        'accion': 'Editar'
    })

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
    data = {'form_is_valid': False}
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            especialidad = form.save(commit=False)
            especialidad.estado = True  # Por defecto activa
            especialidad.save()
            data['form_is_valid'] = True
            especialidades = Especialidad.objects.all().order_by('nombre')
            data['html_especialidad_list'] = render_to_string(
                'profesionales/especialidades/partial_especialidad_list.html',
                {'especialidades': especialidades}
            )
        else:
            data['html_form'] = render_to_string(
                'profesionales/especialidades/includes/partial_especialidad_create.html',
                {'form': form},
                request=request
            )
    else:
        form = EspecialidadForm()
        data['html_form'] = render_to_string(
            'profesionales/especialidades/includes/partial_especialidad_create.html',
            {'form': form},
            request=request
        )
    return JsonResponse(data)

@login_required
def editar_especialidad(request, especialidad_id):
    especialidad = get_object_or_404(Especialidad, id=especialidad_id)
    data = {'form_is_valid': False}
    
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            especialidades = Especialidad.objects.all().order_by('nombre')
            data['html_especialidad_list'] = render_to_string(
                'profesionales/especialidades/partial_especialidad_list.html',
                {'especialidades': especialidades}
            )
        else:
            data['html_form'] = render_to_string(
                'profesionales/especialidades/includes/partial_especialidad_update.html',
                {'form': form, 'especialidad': especialidad},
                request=request
            )
    else:
        form = EspecialidadForm(instance=especialidad)
        data['html_form'] = render_to_string(
            'profesionales/especialidades/includes/partial_especialidad_update.html',
            {'form': form, 'especialidad': especialidad},
            request=request
        )
    return JsonResponse(data)

@login_required
def eliminar_especialidad(request, especialidad_id):
    especialidad = get_object_or_404(Especialidad, id=especialidad_id)
    data = {'form_is_valid': False}
    
    if request.method == 'POST':
        especialidad.delete()
        data['form_is_valid'] = True
        especialidades = Especialidad.objects.all().order_by('nombre')
        data['html_especialidad_list'] = render_to_string(
            'profesionales/especialidades/partial_especialidad_list.html',
            {'especialidades': especialidades}
        )
    else:
        context = {'especialidad': especialidad}
        data['html_form'] = render_to_string(
            'profesionales/especialidades/includes/partial_especialidad_delete.html',
            context,
            request=request
        )
    return JsonResponse(data) 