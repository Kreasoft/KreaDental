from django.conf import settings

def empresa_actual(request):
    empresa_actual = None
    if request.user.is_authenticated:
        from .models import Empresa, UsuarioEmpresa
        
        # Primero intentar obtener la empresa de la sesión
        if 'empresa_actual_id' in request.session:
            try:
                empresa_actual = Empresa.objects.get(
                    id=request.session['empresa_actual_id'],
                    activa=True
                )
            except (Empresa.DoesNotExist, ValueError):
                pass
        
        # Si no hay empresa en sesión, buscar la primera empresa asignada al usuario
        if not empresa_actual:
            usuario_empresa = UsuarioEmpresa.objects.filter(
                usuario=request.user,
                activo=True
            ).first()
            
            if usuario_empresa:
                empresa_actual = usuario_empresa.empresa
                # Guardar en sesión para futuras consultas
                request.session['empresa_actual_id'] = empresa_actual.id
        
        # Si aún no hay empresa, buscar la primera empresa activa disponible
        if not empresa_actual:
            empresa_actual = Empresa.objects.filter(activa=True).first()
            if empresa_actual:
                # Crear relación usuario-empresa si no existe
                UsuarioEmpresa.objects.get_or_create(
                    usuario=request.user,
                    empresa=empresa_actual,
                    defaults={'activo': True}
                )
                # Guardar en sesión
                request.session['empresa_actual_id'] = empresa_actual.id
    
    return {'empresa_actual': empresa_actual}

def sucursal_actual(request):
    """Context processor para obtener la sucursal actual del usuario"""
    sucursal_actual = None
    if request.user.is_authenticated and 'empresa_actual_id' in request.session:
        from .models import Empresa, UsuarioEmpresa
        try:
            empresa = Empresa.objects.get(
                id=request.session['empresa_actual_id'],
                activa=True
            )
            # Obtener la sucursal asignada al usuario en esta empresa
            usuario_empresa = UsuarioEmpresa.objects.filter(
                usuario=request.user,
                empresa=empresa,
                activo=True
            ).first()
            
            if usuario_empresa and usuario_empresa.sucursal:
                sucursal_actual = usuario_empresa.sucursal
        except (Empresa.DoesNotExist, ValueError):
            pass
    return {'sucursal_actual': sucursal_actual}

def sucursales_disponibles(request):
    """Context processor para obtener las sucursales disponibles del usuario"""
    sucursales_disponibles = []
    if request.user.is_authenticated and 'empresa_actual_id' in request.session:
        from .models import Empresa, UsuarioEmpresa, Sucursal
        try:
            empresa = Empresa.objects.get(
                id=request.session['empresa_actual_id'],
                activa=True
            )
            # Obtener todas las sucursales activas de la empresa
            sucursales_disponibles = Sucursal.objects.filter(
                empresa=empresa,
                activa=True
            ).order_by('nombre')
        except (Empresa.DoesNotExist, ValueError):
            pass
    return {'sucursales_disponibles': sucursales_disponibles}
