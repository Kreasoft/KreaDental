from django.urls import path
from . import views

app_name = 'procedimientos'

urlpatterns = [
    path('test/', views.test_template, name='test_template'),
    path('', views.lista_procedimientos, name='lista_procedimientos'),
    path('crear/', views.crear_procedimiento, name='crear_procedimiento'),
    path('editar/<int:procedimiento_id>/', views.editar_procedimiento, name='editar_procedimiento'),
    path('eliminar/<int:procedimiento_id>/', views.eliminar_procedimiento, name='eliminar_procedimiento'),
] 