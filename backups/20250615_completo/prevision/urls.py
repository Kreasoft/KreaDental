from django.urls import path
from . import views

app_name = 'prevision'

urlpatterns = [
    path('', views.lista_previsiones, name='lista_previsiones'),
    path('crear/', views.crear_prevision, name='crear_prevision'),
    path('editar/<int:prevision_id>/', views.editar_prevision, name='editar_prevision'),
    path('eliminar/<int:prevision_id>/', views.eliminar_prevision, name='eliminar_prevision'),
]   
    

    