from django.urls import path
from . import views

app_name = 'tratamientos'

urlpatterns = [
    path('', views.lista_tratamientos, name='lista'),
    path('nuevo/', views.crear_tratamiento, name='crear'),
    path('<int:pk>/', views.detalle_tratamiento, name='detalle'),
    path('<int:pk>/editar/', views.editar_tratamiento, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_tratamiento, name='eliminar'),
    path('<int:pk>/actualizar-estado/', views.actualizar_estado, name='actualizar_estado'),
    path('<int:pk>/marcar-pagado/', views.marcar_pagado, name='marcar_pagado'),
    
    # URLs para pagos
    path('<int:pk>/pagos/', views.pagos_tratamiento, name='pagos_tratamiento'),
    path('pagos/nuevo/', views.nuevo_pago, name='nuevo_pago'),
    path('pagos/<int:pk>/editar/', views.editar_pago, name='editar_pago'),
    path('pagos/<int:pk>/eliminar/', views.eliminar_pago, name='eliminar_pago'),
] 