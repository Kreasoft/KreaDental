from django.urls import path
from . import views

app_name = 'cierres_caja'

urlpatterns = [
    path('', views.lista_cierres, name='lista_cierres'),
    path('abrir/', views.abrir_caja, name='abrir_caja'),
    path('cerrar/<int:cierre_id>/', views.cerrar_caja, name='cerrar_caja'),
    path('detalle/<int:cierre_id>/', views.detalle_cierre, name='detalle_cierre'),
    path('imprimir/<int:cierre_id>/', views.imprimir_cierre, name='imprimir_cierre'),
    
    # URLs para retiros de caja
    path('retiro/<int:cierre_id>/', views.registrar_retiro, name='registrar_retiro'),
    path('retiros/<int:cierre_id>/', views.lista_retiros, name='lista_retiros'),
    path('eliminar-retiro/<int:retiro_id>/', views.eliminar_retiro, name='eliminar_retiro'),
]

default_app_config = 'cierres_caja.apps.CierresCajaConfig'
