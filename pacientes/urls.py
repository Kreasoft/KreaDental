from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.lista_pacientes, name='lista_pacientes'),
    path('nuevo/', views.nuevo_paciente, name='nuevo_paciente'),
    path('editar/<int:pk>/', views.editar_paciente, name='editar_paciente'),
    path('eliminar/<int:pk>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('detalle/<int:pk>/', views.detalle_paciente, name='detalle_paciente'),
    path('cambiar_estado/<int:pk>/', views.cambiar_estado_paciente, name='cambiar_estado_paciente'),
    path('historial/agregar/<int:paciente_id>/', views.agregar_historial, name='agregar_historial'),
    path('historial/editar/<int:pk>/', views.editar_historial, name='editar_historial'),
    path('historial/eliminar/<int:pk>/', views.eliminar_historial, name='eliminar_historial'),
    path('buscar/', views.buscar_pacientes, name='buscar_pacientes'),
] 