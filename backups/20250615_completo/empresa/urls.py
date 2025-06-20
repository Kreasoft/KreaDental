from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import views

# Definir el nombre de la aplicación para el espacio de nombres
app_name = 'empresa'

urlpatterns = [
    # URL de prueba simple (sin autenticación requerida)
    path('test/', lambda request: HttpResponse('¡La URL de prueba funciona!'), name='test'),
    
    # Redirección de la raíz a listar empresas
    path('', login_required(views.listar_empresas), name='index'),
    
    # Creación y selección de empresa
    path('crear-inicial/', views.crear_empresa_inicial, name='crear_empresa_inicial'),
    path('listar/', views.listar_empresas, name='listar_empresas'),
    path('seleccionar/', views.seleccionar_empresa, name='seleccionar_empresa'),
    path('cambiar/<int:empresa_id>/', views.cambiar_empresa, name='cambiar_empresa'),
    
    # Gestión de empresas
    path('editar/<int:empresa_id>/', login_required(views.editar_empresa), name='editar_empresa'),
    path('desactivar/<int:empresa_id>/', login_required(views.desactivar_empresa), name='desactivar_empresa'),
    path('configuracion/', views.configuracion_empresa, name='configuracion_empresa'),
]