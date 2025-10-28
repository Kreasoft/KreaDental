from .models import ConfiguracionEmpresa, PreferenciaUsuario

class ConfiguracionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request.configuracion = ConfiguracionEmpresa.objects.first()
        except:
            request.configuracion = None

        # Agregar preferencias de usuario si está autenticado
        if request.user.is_authenticated:
            try:
                request.preferencias = PreferenciaUsuario.objects.get(usuario=request.user)
            except PreferenciaUsuario.DoesNotExist:
                request.preferencias = PreferenciaUsuario.objects.create(
                    usuario=request.user,
                    fuente='Plus Jakarta Sans'
                )
        
        response = self.get_response(request)

        # Si es una respuesta HTML, inyectar la fuente seleccionada
        if hasattr(request, 'preferencias') and 'text/html' in response.get('Content-Type', ''):
            font_link = f'<link href="https://fonts.googleapis.com/css2?family={request.preferencias.fuente.replace(" ", "+")}:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
            font_style = f'<style>body {{ font-family: "{request.preferencias.fuente}", sans-serif !important; }}</style>'
            
            content = response.content.decode('utf-8')
            head_end = content.find('</head>')
            if head_end > -1:
                content = content[:head_end] + font_link + font_style + content[head_end:]
                response.content = content.encode('utf-8')
        
        return response
