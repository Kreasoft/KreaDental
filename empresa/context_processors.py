from django.conf import settings

def empresa_actual(request):
    empresa_actual = None
    if 'empresa_actual_id' in request.session:
        from .models import Empresa
        try:
            empresa_actual = Empresa.objects.get(
                id=request.session['empresa_actual_id'],
                activo=True
            )
        except (Empresa.DoesNotExist, ValueError):
            pass
    return {'empresa_actual': empresa_actual}
