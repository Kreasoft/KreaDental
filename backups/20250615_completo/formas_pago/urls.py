from django.urls import path
from . import views

app_name = 'formas_pago'

urlpatterns = [
    path('', views.lista_formas_pago, name='lista_formas_pago'),
    path('crear/', views.crear_forma_pago, name='crear_forma_pago'),
    path('editar/<int:pk>/', views.editar_forma_pago, name='editar_forma_pago'),
    path('eliminar/<int:pk>/', views.eliminar_forma_pago, name='eliminar_forma_pago'),
    path('cambiar_estado/<int:pk>/', views.cambiar_estado_forma_pago, name='cambiar_estado_forma_pago'),
]
