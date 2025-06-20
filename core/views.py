from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from pacientes.models import Paciente
from citas.models import Cita
from profesionales.models import Profesional
from configuracion.models import ConfiguracionEmpresa
from datetime import date, timedelta
from django.db.utils import OperationalError
from usuarios.forms import UsuarioCreationForm
from django.contrib import messages
from empresa.models import UsuarioEmpresa, Empresa
from django.utils import timezone
from django.db.models import Count
from especialidades.models import Especialidad



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
    
    # Agregar configuración de la empresa al contexto
    context['empresa'] = ConfiguracionEmpresa.objects.first()
    
    # Debug print
    print("Context:", context)
    
    return render(request, 'core/inicio.html', context)

@login_required
@login_required
def demo_fonts(request):
    from configuracion.models import PreferenciaUsuario
    from django.contrib import messages

    # Obtener o crear las preferencias del usuario
    preferencias, created = PreferenciaUsuario.objects.get_or_create(
        usuario=request.user,
        defaults={'fuente': 'Plus Jakarta Sans'}
    )

    if request.method == 'POST':
        nueva_fuente = request.POST.get('fuente')
        if nueva_fuente in dict(PreferenciaUsuario.FUENTES_DISPONIBLES):
            preferencias.fuente = nueva_fuente
            preferencias.save()
            messages.success(request, 'La fuente del sistema ha sido actualizada.')

    fonts = [
        {
            'nombre': 'Poppins',
            'descripcion': 'Moderna y limpia, perfecta para títulos y contenido. Excelente legibilidad.',
            'familia': '"Poppins", sans-serif',
            'google_font': 'Poppins:wght@300;400;500;600;700',
            'ejemplo': 'Control Dental Moderno'
        },
        {
            'nombre': 'Inter',
            'descripcion': 'Diseñada específicamente para pantallas, con excelente legibilidad en tamaños pequeños.',
            'familia': '"Inter", sans-serif',
            'google_font': 'Inter:wght@300;400;500;600;700',
            'ejemplo': 'Control Dental Moderno'
        },
        {
            'nombre': 'Outfit',
            'descripcion': 'Moderna y geométrica, perfecta para interfaces limpias y profesionales.',
            'familia': '"Outfit", sans-serif',
            'google_font': 'Outfit:wght@300;400;500;600;700',
            'ejemplo': 'Control Dental Moderno'
        },
        {
            'nombre': 'Plus Jakarta Sans',
            'descripcion': 'Contemporánea y profesional, con excelente balance entre modernidad y legibilidad.',
            'familia': '"Plus Jakarta Sans", sans-serif',
            'google_font': 'Plus+Jakarta+Sans:wght@300;400;500;600;700',
            'ejemplo': 'Control Dental Moderno'
        },
        {
            'nombre': 'DM Sans',
            'descripcion': 'Minimalista y moderna, ideal para interfaces médicas y profesionales.',
            'familia': '"DM Sans", sans-serif',
            'google_font': 'DM+Sans:wght@300;400;500;600;700',
            'ejemplo': 'Control Dental Moderno'
        }
    ]
    return render(request, 'core/demo_fonts.html', {
        'fonts': fonts,
        'fuente_actual': preferencias.fuente
    })

@login_required
def home(request):
    # Obtener estadísticas básicas
    total_profesionales = Profesional.objects.filter(activo=True).count()
    total_pacientes = Paciente.objects.filter(activo=True).count()
    citas_hoy = Cita.objects.filter(
        fecha=timezone.now().date(),
        estado='PENDIENTE'
    ).count()
    total_especialidades = Especialidad.objects.filter(estado=True).count()
    
    # Estadísticas adicionales
    profesionales_activos = Profesional.objects.filter(activo=True).count()
    pacientes_mes = Paciente.objects.filter(
        fecha_registro__month=timezone.now().month,
        fecha_registro__year=timezone.now().year,
        activo=True
    ).count()
    citas_pendientes = Cita.objects.filter(estado='PENDIENTE').count()
    
    # Obtener la empresa actual
    empresa_actual = Empresa.objects.filter(activa=True).first()
    
    # Obtener la sucursal activa del usuario
    sucursal_activa = None
    if empresa_actual:
        # Buscar la sucursal activa del usuario en esta empresa
        usuario_empresa = UsuarioEmpresa.objects.filter(
            usuario=request.user,
            empresa=empresa_actual,
            activo=True
        ).first()
        
        if usuario_empresa and usuario_empresa.sucursal:
            sucursal_activa = usuario_empresa.sucursal
    
    # Obtener las próximas citas
    proximas_citas = Cita.objects.filter(
        fecha__gte=timezone.now().date(),
        estado='PENDIENTE'
    ).order_by('fecha', 'hora')[:5]
    
    context = {
        'total_profesionales': total_profesionales,
        'total_pacientes': total_pacientes,
        'citas_hoy': citas_hoy,
        'total_especialidades': total_especialidades,
        'profesionales_activos': profesionales_activos,
        'pacientes_mes': pacientes_mes,
        'citas_pendientes': citas_pendientes,
        'empresa_actual': empresa_actual,
        'sucursal_activa': sucursal_activa,
        'proximas_citas': proximas_citas,
    }
    
    return render(request, 'core/home.html', context)

def register(request):
    # Obtener la configuración de la empresa
    empresa = ConfiguracionEmpresa.objects.first()
    
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Iniciar sesión automáticamente
            login(request, user)
            return redirect('home')
    else:
        form = UsuarioCreationForm()
    
    return render(request, 'core/register.html', {
        'form': form,
        'empresa': empresa
    })

@login_required
def colores_calipso(request):
    return render(request, 'colores_calipso.html')