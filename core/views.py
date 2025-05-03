from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente
from citas.models import Cita
from profesionales.models import Profesional
from datetime import date, timedelta

@login_required
def index(request):
    # Obtener estadísticas generales
    total_pacientes = Paciente.objects.count()
    total_profesionales = Profesional.objects.count()
    
    # Obtener citas del día
    citas_hoy = Cita.objects.filter(fecha=date.today())
    total_citas_hoy = citas_hoy.count()
    
    # Obtener citas pendientes para los próximos 7 días
    fecha_fin = date.today() + timedelta(days=7)
    citas_proximas = Cita.objects.filter(
        fecha__range=[date.today(), fecha_fin],
        estado='PENDIENTE'
    ).order_by('fecha', 'hora')
    
    # Obtener citas por estado
    citas_por_estado = {
        'PENDIENTE': Cita.objects.filter(estado='PENDIENTE').count(),
        'CONFIRMADA': Cita.objects.filter(estado='CONFIRMADA').count(),
        'COMPLETADA': Cita.objects.filter(estado='COMPLETADA').count(),
        'CANCELADA': Cita.objects.filter(estado='CANCELADA').count()
    }
    
    return render(request, 'core/index.html', {
        'total_pacientes': total_pacientes,
        'total_profesionales': total_profesionales,
        'total_citas_hoy': total_citas_hoy,
        'citas_proximas': citas_proximas,
        'citas_por_estado': citas_por_estado
    })

@login_required
def inicio(request):
    # Obtener conteos
    context = {
        'total_pacientes': Paciente.objects.count(),
        'total_citas': Cita.objects.count(),
        'total_profesionales': Profesional.objects.count(),
    }
    
    # Obtener citas por estado
    citas_por_estado = {
        'PENDIENTE': Cita.objects.filter(estado='PENDIENTE').count(),
        'CONFIRMADA': Cita.objects.filter(estado='CONFIRMADA').count(),
        'COMPLETADA': Cita.objects.filter(estado='COMPLETADA').count(),
        'CANCELADA': Cita.objects.filter(estado='CANCELADA').count()
    }
    
    # Agregar datos de estados al contexto
    context['citas_por_estado'] = citas_por_estado
    
    # Debug print
    print("Context:", context)
    
    return render(request, 'core/inicio.html', context)

@login_required
def home(request):
    # Obtener estadísticas generales
    total_pacientes = Paciente.objects.count()
    total_profesionales = Profesional.objects.count()
    
    # Obtener citas del día
    citas_hoy = Cita.objects.filter(fecha=date.today())
    total_citas_hoy = citas_hoy.count()
    
    # Obtener citas pendientes para los próximos 7 días
    fecha_fin = date.today() + timedelta(days=7)
    citas_proximas = Cita.objects.filter(
        fecha__range=[date.today(), fecha_fin],
        estado='PENDIENTE'
    ).order_by('fecha', 'hora')
    
    # Obtener citas por estado
    citas_por_estado = {
        'PENDIENTE': Cita.objects.filter(estado='PENDIENTE').count(),
        'CONFIRMADA': Cita.objects.filter(estado='CONFIRMADA').count(),
        'COMPLETADA': Cita.objects.filter(estado='COMPLETADA').count(),
        'CANCELADA': Cita.objects.filter(estado='CANCELADA').count()
    }
    
    return render(request, 'core/home_simple.html', {
        'total_pacientes': total_pacientes,
        'total_profesionales': total_profesionales,
        'total_citas_hoy': total_citas_hoy,
        'citas_proximas': citas_proximas,
        'citas_por_estado': citas_por_estado
    }) 