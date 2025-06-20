from django.urls import path
from . import views

app_name = 'tratamientos'


urlpatterns = [
    path('', views.lista_tratamientos, name='lista_tratamientos'),
    path('crear/', views.crear_tratamiento, name='crear_tratamiento'),
    path('<int:pk>/', views.detalle_tratamiento, name='detalle_tratamiento'),
    path('<int:pk>/editar/', views.editar_tratamiento, name='editar_tratamiento'),
    path('<int:pk>/eliminar/', views.eliminar_tratamiento, name='eliminar_tratamiento'),
    path('<int:pk>/actualizar-estado/', views.actualizar_estado, name='actualizar_estado'),
    path('<int:pk>/marcar-pagado/', views.marcar_pagado, name='marcar_pagado'),
] 