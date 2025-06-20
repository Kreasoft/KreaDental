from django.urls import path
from . import views

app_name = 'cierres_caja'

urlpatterns = [
    path('', views.lista_cierres, name='lista_cierres'),
    path('abrir/', views.abrir_caja, name='abrir_caja'),
    path('cerrar/<int:cierre_id>/', views.cerrar_caja, name='cerrar_caja'),
    path('detalle/<int:cierre_id>/', views.detalle_cierre, name='detalle_cierre'),
]

default_app_config = 'cierres_caja.apps.CierresCajaConfig'
