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
    path('eliminar/<int:empresa_id>/', login_required(views.eliminar_empresa), name='eliminar_empresa'),
    path('configuracion/', views.configuracion_empresa, name='configuracion_empresa'),
    
    # Gestión de sucursales
    path('<int:empresa_id>/sucursales/', login_required(views.listar_sucursales), name='listar_sucursales'),
    path('<int:empresa_id>/sucursales/crear/', login_required(views.crear_sucursal), name='crear_sucursal'),
    path('<int:empresa_id>/sucursales/<int:sucursal_id>/editar/', login_required(views.editar_sucursal), name='editar_sucursal'),
    path('<int:empresa_id>/sucursales/<int:sucursal_id>/eliminar/', login_required(views.eliminar_sucursal), name='eliminar_sucursal'),
    
    # Usuarios
    path('<int:empresa_id>/usuarios/', views.listar_usuarios_empresa, name='listar_usuarios_empresa'),
    path('<int:empresa_id>/usuarios/crear/', views.crear_usuario_empresa, name='crear_usuario_empresa'),
    path('<int:empresa_id>/usuarios/<int:usuario_empresa_id>/editar/', views.editar_usuario_empresa, name='editar_usuario_empresa'),
    path('<int:empresa_id>/usuarios/<int:usuario_empresa_id>/eliminar/', views.eliminar_usuario_empresa, name='eliminar_usuario_empresa'),
    
    # Cambiar sucursal
    path('cambiar-sucursal/<int:sucursal_id>/', views.cambiar_sucursal, name='cambiar_sucursal'),
]