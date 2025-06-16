from django.urls import path
from . import views

app_name = 'lab_dental'

urlpatterns = [
    # URLs para Laboratorios
    path('laboratorios/', views.lista_laboratorios, name='lista_laboratorios'),
    path('laboratorios/crear/', views.crear_laboratorio, name='crear_laboratorio'),
    path('laboratorios/<int:pk>/', views.detalle_laboratorio, name='detalle_laboratorio'),
    path('laboratorios/<int:pk>/editar/', views.editar_laboratorio, name='editar_laboratorio'),
    
    # URLs para Trabajos de Laboratorio
    path('trabajos/', views.lista_trabajos, name='lista_trabajos'),
    path('trabajos/crear/', views.crear_trabajo, name='crear_trabajo'),
    path('trabajos/<int:pk>/', views.detalle_trabajo, name='detalle_trabajo'),
]
