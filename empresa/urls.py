from django.urls import path
from . import views

app_name = 'empresa'

urlpatterns = [
    path('', views.editar_empresa, name='editar_empresa'),  # Solo necesitamos una vista para editar la empresa
] 