from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.lista_citas, name='lista_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),
    path('eliminar/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('informes/', views.informes, name='informes'),
    path('calendario/', views.calendario_citas, name='calendario_citas'),
    path('calendario/obtener/', views.obtener_citas, name='obtener_citas'),
    path('calendario/guardar/', views.guardar_cita, name='guardar_cita'),
] 