from django.urls import path
from . import views

app_name = 'configuracion'

urlpatterns = [
    path('empresa/', views.configuracion_empresa, name='empresa'),
    path('', views.configuracion_empresa, name='index'),  # URL por defecto
]
