from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class EmpresaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Rutas que no requieren empresa
        rutas_excluidas = [
            '/login/',
            '/logout/',
            '/empresas/',
            '/admin/',
            '/static/',
            '/media/',
            '/favicon.ico',
        ]
        
        # Solo verificar empresa para rutas que no están excluidas
        if (request.user.is_authenticated and 
            not any(request.path.startswith(ruta) for ruta in rutas_excluidas)):
            
            # Verificar si tiene empresa seleccionada
            empresa_id = request.session.get('empresa_actual_id') or request.session.get('empresa_id')
            
            if not empresa_id:
                # Solo redirigir si no está ya en una página de empresa
                if not request.path.startswith('/empresas/'):
                    return redirect('empresa:seleccionar_empresa')
                    
        response = self.get_response(request)
        return response
