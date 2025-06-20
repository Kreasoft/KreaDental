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
            '/seleccionar-empresa/',
            '/admin/',
            '/static/',
            '/media/',
            '/favicon.ico',
        ]
        
        if (request.user.is_authenticated and 
            not any(request.path.startswith(ruta) for ruta in rutas_excluidas)):
            
            # Si no tiene empresa seleccionada, redirigir a selección
            if 'empresa_actual_id' not in request.session:
                return redirect('seleccionar_empresa')
                    
        response = self.get_response(request)
        return response
