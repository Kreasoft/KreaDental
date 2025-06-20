from django.shortcuts import get_object_or_404
from .models import Empresa

def get_empresa_actual(request):
    """
    Obtiene la empresa actual del usuario desde la sesión.
    Si no hay empresa seleccionada, devuelve la primera empresa del usuario.
    """
    empresa_id = request.session.get('empresa_id')
    if empresa_id:
        return get_object_or_404(Empresa, id=empresa_id)
    return None 