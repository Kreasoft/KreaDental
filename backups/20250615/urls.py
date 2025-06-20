from django.urls import path
from . import views

app_name = 'profesionales'

urlpatterns = [
    path('', views.lista_profesionales, name='lista_profesionales'),
    path('nuevo/', views.nuevo_profesional, name='nuevo_profesional'),
    path('editar/<int:pk>/', views.editar_profesional, name='editar_profesional'),
    path('eliminar/<int:pk>/', views.eliminar_profesional, name='eliminar_profesional'),
    
    # URLs para Especialidades
    path('especialidades/', views.lista_especialidades, name='lista_especialidades'),
    path('especialidades/crear/', views.crear_especialidad, name='crear_especialidad'),
    path('especialidades/editar/<int:especialidad_id>/', views.editar_especialidad, name='editar_especialidad'),
    path('especialidades/eliminar/<int:especialidad_id>/', views.eliminar_especialidad, name='eliminar_especialidad'),
] 