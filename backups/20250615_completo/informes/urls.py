from django.urls import path
from . import views

app_name = 'informes'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tratamientos/', views.informe_tratamientos, name='tratamientos'),
    path('financiero/', views.informe_financiero, name='financiero'),
    path('pacientes/', views.informe_pacientes, name='pacientes'),
]
