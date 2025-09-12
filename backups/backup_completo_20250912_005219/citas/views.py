from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Cita
from .forms import CitaForm
from profesionales.models import Profesional
from pacientes.models import Paciente
from datetime import datetime
from empresa.utils import get_empresa_actual
import json
from django.db.models import Q

@login_required
def informes(request):
    """Vista para mostrar los informes de citas"""
    return render(request, 'citas/informes.html')

@login_required
def calendario_citas(request):
    # Obtener la empresa actual del usuario
    empresa_actual = get_empresa_actual(request)
    
    # Filtrar profesionales: propios + compartidos conmigo
    profesionales = Profesional.objects.filter(
        Q(empresa=empresa_actual, activo=True) | 
        Q(empresas_compartidas=empresa_actual, compartir_entre_sucursales=True, activo=True)
    ).distinct().order_by('apellido_paterno', 'apellido_materno', 'nombres')
    
    # Filtrar pacientes: propios + compartidos conmigo
    pacientes = Paciente.objects.filter(
        Q(empresa=empresa_actual, activo=True) | 
        Q(empresas_compartidas=empresa_actual, compartir_entre_sucursales=True, activo=True)
    ).distinct().order_by('apellidos', 'nombre')
    
    profesional_id = request.GET.get('profesional')
    
    # Crear el formulario con los querysets filtrados
    form = CitaForm()
    form.fields['profesional'].queryset = profesionales
    form.fields['paciente'].queryset = pacientes
    
    if profesional_id:
        try:
            profesional_seleccionado = profesionales.get(id=profesional_id)
        except Profesional.DoesNotExist:
            profesional_seleccionado = None
    else:
        profesional_seleccionado = None
    
    context = {
        'form': form,
        'profesionales': profesionales,
        'pacientes': pacientes,
        'profesional_seleccionado': profesional_seleccionado,
        'empresa_actual': empresa_actual,
    }
    
    return render(request, 'citas/calendario_citas.html', context)

@login_required
def guardar_cita(request):
    if request.method == 'POST':
        print("Recibiendo POST request para guardar cita")
        print("Datos recibidos:", request.POST)
        
        try:
            # Obtener la empresa actual del usuario
            empresa_actual = get_empresa_actual(request)
            
            # Obtener el ID de la cita si existe (para edición)
            cita_id = request.POST.get('cita_id')
            instance = None
            if cita_id:
                instance = get_object_or_404(Cita, pk=cita_id)
            
            # Obtener datos del formulario
            form = CitaForm(request.POST, instance=instance)
            
            # Filtrar los querysets por empresa
            profesionales = Profesional.objects.filter(
                empresa=empresa_actual,
                activo=True
            ).order_by('apellido_paterno', 'apellido_materno', 'nombres')
            
            pacientes = Paciente.objects.filter(
                empresa=empresa_actual,
                activo=True
            ).order_by('apellidos', 'nombre')
            
            form.fields['profesional'].queryset = profesionales
            form.fields['paciente'].queryset = pacientes
            
            print("Formulario creado")
            
            if form.is_valid():
                print("Formulario válido")
                try:
                    cita = form.save(commit=False)
                    print("Cita creada:", cita)
                    print("Datos de la cita:")
                    print(f"Paciente: {cita.paciente}")
                    print(f"Profesional: {cita.profesional}")
                    print(f"Fecha: {cita.fecha}")
                    print(f"Hora: {cita.hora}")
                    print(f"Duración: {cita.duracion}")
                    print(f"Estado: {cita.estado}")
                    
                    # Validar que no haya citas solapadas
                    hora_fin = cita.get_hora_fin()
                    print(f"Hora fin calculada: {hora_fin}")
                    
                    citas_solapadas = Cita.objects.filter(
                        profesional=cita.profesional,
                        fecha=cita.fecha,
                        hora__lt=hora_fin,
                        hora__gt=cita.hora
                    ).exclude(pk=cita.pk if cita.pk else None)
                    
                    if citas_solapadas.exists():
                        print("Cita solapada encontrada")
                        return JsonResponse({
                            'success': False,
                            'errors': {
                                'general': ['Ya existe una cita programada en ese horario para este profesional.']
                            }
                        })
                    
                    cita.save()
                    print("Cita guardada exitosamente")
                    
                    return JsonResponse({
                        'success': True,
                        'id': cita.id,
                        'message': 'Cita guardada correctamente'
                    })
                except Exception as e:
                    print(f"Error al guardar la cita: {str(e)}")
                    print(f"Tipo de error: {type(e)}")
                    import traceback
                    print("Traceback completo:")
                    print(traceback.format_exc())
                    return JsonResponse({
                        'success': False,
                        'errors': {'general': [f'Error al guardar la cita: {str(e)}']}
                    })
            else:
                print("Formulario inválido")
                print("Errores del formulario:", form.errors)
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
        except Exception as e:
            print(f"Error general: {str(e)}")
            print(f"Tipo de error: {str(type(e))}")
            import traceback
            print("Traceback completo:")
            print(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'errors': {'general': [f'Error al procesar la solicitud: {str(e)}']}
            })
    
    return JsonResponse({
        'success': False,
        'errors': {'general': ['Método no permitido']}
    }, status=405)

@login_required
def obtener_citas(request):
    try:
        # Obtener la empresa actual del usuario
        empresa_actual = get_empresa_actual(request)
        
        profesional_id = request.GET.get('profesional')
        estado = request.GET.get('estado')
        fecha_inicio = request.GET.get('start')
        fecha_fin = request.GET.get('end')
        
        # Filtrar citas por empresa actual
        citas = Cita.objects.select_related('paciente', 'profesional').filter(
            profesional__empresa=empresa_actual
        )
        
        if profesional_id:
            citas = citas.filter(profesional_id=profesional_id)
        
        if estado:
            citas = citas.filter(estado=estado)
        
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                citas = citas.filter(fecha__gte=fecha_inicio)
            except ValueError:
                pass
                
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                citas = citas.filter(fecha__lte=fecha_fin)
            except ValueError:
                pass
        
        events = []
        for cita in citas:
            try:
                hora_inicio = cita.hora.strftime('%H:%M:%S')
                hora_fin = cita.get_hora_fin().strftime('%H:%M:%S')
                
                events.append({
                    'id': cita.id,
                    'title': f'{cita.paciente.nombre_completo()}',
                    'start': f'{cita.fecha}T{hora_inicio}',
                    'end': f'{cita.fecha}T{hora_fin}',
                    'backgroundColor': {
                        'PENDIENTE': '#FFD700',    # Dorado suave
                        'CONFIRMADA': '#90EE90',   # Verde claro
                        'COMPLETADA': '#87CEEB',   # Azul claro
                        'CANCELADA': '#FFB6C1'     # Rosa claro
                    }.get(cita.estado, '#6c757d'),
                    'className': f'fc-event-{cita.estado.lower()}',
                    'extendedProps': {
                        'paciente_id': cita.paciente.id,
                        'paciente': cita.paciente.nombre_completo(),
                        'profesional_id': cita.profesional.id,
                        'profesional': cita.profesional.nombre_completo(),
                        'duracion': cita.duracion,
                        'estado': cita.estado,
                        'motivo': cita.motivo,
                        'estado_display': cita.get_estado_display()
                    }
                })
            except Exception as e:
                print(f"Error al procesar cita {cita.id}: {str(e)}")
                continue
        
        return JsonResponse(events, safe=False)
    except Exception as e:
        print(f"Error en obtener_citas: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def lista_citas(request):
    """Vista para mostrar el calendario de citas"""
    # Obtener la empresa actual del usuario
    empresa_actual = get_empresa_actual(request)
    
    # Filtrar citas por empresa actual
    citas = Cita.objects.select_related('paciente', 'profesional').filter(
        profesional__empresa=empresa_actual
    )
    
    return render(request, 'citas/lista_citas.html', {
        'citas': citas
    })

@login_required
def crear_cita(request):
    """Vista para crear una nueva cita"""
    # Obtener la empresa actual del usuario
    empresa_actual = get_empresa_actual(request)
    
    # Filtrar profesionales y pacientes por empresa
    profesionales = Profesional.objects.filter(
        empresa=empresa_actual,
        activo=True
    ).order_by('apellido_paterno', 'apellido_materno', 'nombres')
    
    pacientes = Paciente.objects.filter(
        empresa=empresa_actual,
        activo=True
    ).order_by('apellidos', 'nombre')
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        # Establecer los querysets filtrados
        form.fields['profesional'].queryset = profesionales
        form.fields['paciente'].queryset = pacientes
        
        if form.is_valid():
            try:
                cita = form.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'id': cita.id,
                        'message': 'Cita creada correctamente'
                    })
                messages.success(request, 'Cita creada correctamente.')
                return redirect('citas:calendario_citas')
            except Exception as e:
                print(f"Error al guardar la cita: {str(e)}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': {'general': [f'Error al guardar la cita: {str(e)}']}
                    })
                messages.error(request, f'Error al guardar la cita: {str(e)}')
                return redirect('citas:crear_cita')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        initial = {}
        if request.GET.get('fecha'):
            initial['fecha'] = request.GET.get('fecha')
        if request.GET.get('hora'):
            initial['hora'] = request.GET.get('hora')
        form = CitaForm(initial=initial)
        # Establecer los querysets filtrados
        form.fields['profesional'].queryset = profesionales
        form.fields['paciente'].queryset = pacientes
    
    return render(request, 'citas/form_cita.html', {
        'form': form,
        'accion': 'Crear'
    })

@login_required
def editar_cita(request, cita_id):
    """Vista para editar una cita existente"""
    # Obtener la empresa actual del usuario
    empresa_actual = get_empresa_actual(request)
    
    # Obtener la cita y verificar que pertenezca a la empresa actual
    cita = get_object_or_404(Cita, id=cita_id, profesional__empresa=empresa_actual)
    
    # Filtrar profesionales y pacientes por empresa
    profesionales = Profesional.objects.filter(
        empresa=empresa_actual,
        activo=True
    ).order_by('apellido_paterno', 'apellido_materno', 'nombres')
    
    pacientes = Paciente.objects.filter(
        empresa=empresa_actual,
        activo=True
    ).order_by('apellidos', 'nombre')
    
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        # Establecer los querysets filtrados
        form.fields['profesional'].queryset = profesionales
        form.fields['paciente'].queryset = pacientes
        
        if form.is_valid():
            try:
                cita = form.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'id': cita.id,
                        'message': 'Cita actualizada correctamente'
                    })
                messages.success(request, 'Cita actualizada correctamente.')
                return redirect('citas:calendario_citas')
            except Exception as e:
                print(f"Error al actualizar la cita: {str(e)}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': {'general': [f'Error al actualizar la cita: {str(e)}']}
                    })
                messages.error(request, f'Error al actualizar la cita: {str(e)}')
                return redirect('citas:editar_cita', cita_id=cita.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = CitaForm(instance=cita)
        # Establecer los querysets filtrados
        form.fields['profesional'].queryset = profesionales
        form.fields['paciente'].queryset = pacientes
    
    return render(request, 'citas/form_cita.html', {
        'form': form,
        'cita': cita,
        'accion': 'Editar'
    })

@login_required
def eliminar_cita(request, cita_id):
    """Vista para eliminar una cita existente"""
    # Obtener la empresa actual del usuario
    empresa_actual = get_empresa_actual(request)
    
    # Obtener la cita y verificar que pertenezca a la empresa actual
    cita = get_object_or_404(Cita, id=cita_id, profesional__empresa=empresa_actual)
    
    if request.method == 'POST':
        try:
            cita.delete()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Cita eliminada correctamente'
                })
            messages.success(request, 'Cita eliminada correctamente.')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': {'general': [f'Error al eliminar la cita: {str(e)}']}
                })
            messages.error(request, f'Error al eliminar la cita: {str(e)}')
        return redirect('citas:calendario_citas')
    
    return render(request, 'citas/confirmar_eliminar.html', {
        'cita': cita
    }) 