from django.urls import path
from . import views

app_name = 'pagos_tratamientos'

urlpatterns = [
    path('', views.lista_pagos, name='lista_pagos'),
    path('crear/<int:tratamiento_id>/', views.crear_pago, name='crear_pago'),
    path('anular/<int:pago_id>/', views.anular_pago, name='anular_pago'),
    path('detalle/<int:pago_id>/', views.detalle_pago, name='detalle_pago'),
    path('editar/<int:pago_id>/', views.editar_pago, name='editar_pago'),
]
