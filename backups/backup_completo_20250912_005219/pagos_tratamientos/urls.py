from django.urls import path
from . import views

app_name = 'pagos_tratamientos'

urlpatterns = [
    path('', views.lista_pagos, name='lista_pagos'),
    path('agregar/', views.agregar_pago_simple, name='agregar_pago_simple'),
    path('crear/<int:tratamiento_id>/', views.crear_pago, name='crear_pago'),
    path('anular/<int:pago_id>/', views.anular_pago, name='anular_pago'),
    path('detalle/<int:pago_id>/', views.detalle_pago, name='detalle_pago'),
    path('editar/<int:pago_id>/', views.editar_pago, name='editar_pago'),
    path('exportar/', views.exportar_pagos, name='exportar_pagos'),
    path('resumen/<int:pago_id>/', views.resumen_tratamiento, name='resumen_tratamiento'),
    
    # URLs para pagos de atenciones únicas
    path('atenciones/', views.lista_pagos_atenciones, name='lista_pagos_atenciones'),
    path('atenciones/agregar/<int:cita_id>/', views.agregar_pago_atencion, name='agregar_pago_atencion'),
    path('atenciones/rapido/', views.agregar_pago_atencion_rapido, name='agregar_pago_atencion_rapido'),
    path('atenciones/editar/<int:pago_id>/', views.editar_pago_atencion, name='editar_pago_atencion'),
    path('atenciones/anular/<int:pago_id>/', views.anular_pago_atencion, name='anular_pago_atencion'),
    path('estado-cuenta/<int:paciente_id>/', views.estado_cuenta_paciente, name='estado_cuenta_paciente'),
]