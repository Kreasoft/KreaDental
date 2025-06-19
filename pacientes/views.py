from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Paciente, HistorialClinico, Profesional
from .forms import PacienteForm, HistorialClinicoForm
from prevision.models import Prevision
from tratamientos.models import Tratamiento
import json

@login_required
def lista_pacientes(request):
    # Obtener la empresa actual del usuario a través de UsuarioEmpresa
    usuario_empresa = request.user.usuarioempresa_set.filter(activo=True).first()
    empresa_actual = usuario_empresa.empresa if usuario_empresa else None
    
    if not empresa_actual:
        messages.error(request, 'No tienes una empresa asignada.')
        return redirect('home')
    
    # Obtener pacientes de la empresa actual
    pacientes = Paciente.objects.filter(empresa=empresa_actual).order_by('apellidos', 'nombre')
    
    # Estadísticas
    total_pacientes = pacientes.count()
    pacientes_activos = pacientes.filter(activo=True).count()
    
    # Pacientes nuevos este mes
    primer_dia_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    pacientes_nuevos = pacientes.filter(fecha_registro__gte=primer_dia_mes).count()
    
    # Citas pendientes
    hoy = timezone.now()
    citas_pendientes = Tratamiento.objects.filter(
        paciente__in=pacientes,
        fecha_inicio__gte=hoy,
        estado='PENDIENTE'
    ).count()
    
    # Obtener todas las previsiones para el filtro
    previsiones = Prevision.objects.all().order_by('nombre')
    
    context = {
        'pacientes': pacientes,
        'total_pacientes': total_pacientes,
        'pacientes_activos': pacientes_activos,
        'pacientes_nuevos': pacientes_nuevos,
        'citas_pendientes': citas_pendientes,
        'previsiones': previsiones,
        'empresa_actual': empresa_actual,
    }
    
    return render(request, 'pacientes/lista_pacientes.html', context)

@login_required
def nuevo_paciente(request):
    # Obtener la empresa actual del usuario
    usuario_empresa = request.user.usuarioempresa_set.filter(activo=True).first()
    empresa_actual = usuario_empresa.empresa if usuario_empresa else None
    
    if not empresa_actual:
        messages.error(request, 'No tienes una empresa asignada.')
        return redirect('home')

    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            try:
                paciente = form.save(commit=False)
                paciente.empresa = empresa_actual
                paciente.save()
                messages.success(request, 'Paciente creado correctamente.')
                return redirect('pacientes:lista_pacientes')
            except Exception as e:
                messages.error(request, f'Error al crear el paciente: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = PacienteForm()
    
    # Obtener todas las previsiónes para el select
    from prevision.models import Prevision
    previsiones = Prevision.objects.all().order_by('nombre')
    
    return render(request, 'pacientes/form_paciente.html', {
        'form': form,
        'accion': 'Nuevo',
        'previsiones': previsiones
    })

@login_required
def editar_paciente(request, pk):
    # Obtener la empresa actual del usuario
    usuario_empresa = request.user.usuarioempresa_set.filter(activo=True).first()
    empresa_actual = usuario_empresa.empresa if usuario_empresa else None
    
    if not empresa_actual:
        messages.error(request, 'No tienes una empresa asignada.')
        return redirect('home')

    paciente = get_object_or_404(Paciente, pk=pk, empresa=empresa_actual)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Paciente actualizado correctamente.')
                return redirect('pacientes:lista_pacientes')
            except Exception as e:
                messages.error(request, f'Error al actualizar el paciente: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = PacienteForm(instance=paciente)
    
    # Obtener todas las previsiónes para el select
    from prevision.models import Prevision
    previsiones = Prevision.objects.all().order_by('nombre')
    
    return render(request, 'pacientes/form_paciente.html', {
        'form': form,
        'paciente': paciente,
        'accion': 'Editar',
        'previsiones': previsiones
    })

@login_required
def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        paciente.delete()
        return redirect('pacientes:lista_pacientes')
    return render(request, 'pacientes/confirmar_eliminar.html', {'paciente': paciente})

def paciente_list(request):
    pacientes = Paciente.objects.all().order_by('-id')
    return render(request, 'pacientes/paciente_list.html', {
        'pacientes': pacientes
    })

def paciente_create(request):
    data = dict()
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            pacientes = Paciente.objects.all()
            data['html_paciente_list'] = render_to_string(
                'pacientes/includes/partial_paciente_list.html',
                {'pacientes': pacientes}
            )
        else:
            data['form_is_valid'] = False
    else:
        form = PacienteForm()
    
    data['html_form'] = render_to_string(
        'pacientes/includes/partial_paciente_create.html',
        {'form': form},
        request=request
    )
    return JsonResponse(data)

def paciente_update(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    data = dict()
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            pacientes = Paciente.objects.all()
            data['html_paciente_list'] = render_to_string(
                'pacientes/includes/partial_paciente_list.html',
                {'pacientes': pacientes}
            )
        else:
            data['form_is_valid'] = False
    else:
        form = PacienteForm(instance=paciente)
    
    data['html_form'] = render_to_string(
        'pacientes/includes/partial_paciente_update.html',
        {'form': form, 'paciente': paciente},
        request=request
    )
    return JsonResponse(data)

def paciente_delete(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    data = dict()
    if request.method == 'POST':
        paciente.delete()
        data['form_is_valid'] = True
        pacientes = Paciente.objects.all()
        data['html_paciente_list'] = render_to_string(
            'pacientes/includes/partial_paciente_list.html',
            {'pacientes': pacientes}
        )
    else:
        data['html_form'] = render_to_string(
            'pacientes/includes/partial_paciente_delete.html',
            {'paciente': paciente},
            request=request
        )
    return JsonResponse(data)

@login_required
@require_POST
@csrf_exempt
def cambiar_estado_paciente(request, pk):
    try:
        paciente = get_object_or_404(Paciente, pk=pk)
        data = json.loads(request.body)
        paciente.activo = data.get('activo', False)
        paciente.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def agregar_historial(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST, request.FILES)
        if form.is_valid():
            historial = form.save(commit=False)
            historial.paciente = paciente
            # Obtener el Profesional asociado al usuario usando la relación inversa
            profesional = request.user.profesional_relacionado
            if profesional:
                historial.profesional = profesional
            historial.save()
            messages.success(request, 'Registro clínico agregado exitosamente.')
            return redirect('pacientes:editar_paciente', pk=paciente.id)
    else:
        form = HistorialClinicoForm()
    return render(request, 'pacientes/agregar_historial.html', {
        'form': form,
        'paciente': paciente
    })

@login_required
def editar_historial(request, pk):
    historial = get_object_or_404(HistorialClinico, id=pk)
    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST, request.FILES, instance=historial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro clínico actualizado exitosamente.')
            return redirect('pacientes:editar_paciente', pk=historial.paciente.id)
    else:
        form = HistorialClinicoForm(instance=historial)
    return render(request, 'pacientes/editar_historial.html', {
        'form': form,
        'historial': historial
    })

@login_required
def eliminar_historial(request, pk):
    historial = get_object_or_404(HistorialClinico, id=pk)
    paciente_id = historial.paciente.id
    historial.delete()
    messages.success(request, 'Registro clínico eliminado exitosamente.')
    return redirect('pacientes:editar_paciente', pk=paciente_id)

@login_required
def buscar_pacientes(request):
    """Vista para búsqueda de pacientes con Select2"""
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    # Número de resultados por página
    page_size = 10
    offset = (page - 1) * page_size
    
    # Realizar la búsqueda
    if query:
        pacientes = Paciente.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(documento__icontains=query)
        ).order_by('apellidos', 'nombre')[offset:offset + page_size]
    else:
        pacientes = Paciente.objects.all().order_by('apellidos', 'nombre')[offset:offset + page_size]
    
    # Formatear resultados para Select2
    results = [{
        'id': paciente.id,
        'nombre': paciente.nombre,
        'apellidos': paciente.apellidos,
        'documento': paciente.documento
    } for paciente in pacientes]
    
    return JsonResponse({
        'results': results,
        'pagination': {
            'more': len(results) == page_size
        }
    })

@login_required
def detalle_paciente(request, pk):
    # Obtener la empresa actual del usuario
    usuario_empresa = request.user.usuarioempresa_set.filter(activo=True).first()
    empresa_actual = usuario_empresa.empresa if usuario_empresa else None
    
    if not empresa_actual:
        messages.error(request, 'No tienes una empresa asignada.')
        return redirect('home')

    paciente = get_object_or_404(Paciente, pk=pk, empresa=empresa_actual)
    # Usar el related_name correcto
    historiales = paciente.historiales_clinicos.all().order_by('-fecha')
    
    context = {
        'paciente': paciente,
        'historiales': historiales,
        'empresa_actual': empresa_actual,
    }
    
    return render(request, 'pacientes/detalle_paciente.html', context)