from django.shortcuts import get_object_or_404
from .models import Empresa, UsuarioEmpresa

def get_empresa_actual(request):
    """
    Obtiene la empresa actual del usuario desde la sesión.
    Si no hay empresa seleccionada, devuelve la primera empresa del usuario.
    """
    empresa_actual = None
    if request.user.is_authenticated:
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
    
    return empresa_actual 