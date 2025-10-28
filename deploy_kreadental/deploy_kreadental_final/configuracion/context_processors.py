from .models import ConfiguracionEmpresa

def configuracion_empresa(request):
    """Agrega la configuración de la empresa al contexto de todos los templates."""
    try:
        configuracion = ConfiguracionEmpresa.objects.first()
    except:
        configuracion = None
    
    return {
        'configuracion': configuracion
    }
