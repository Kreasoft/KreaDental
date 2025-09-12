from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('demo-fonts/', views.demo_fonts, name='demo_fonts'),
    path('colores-calipso/', views.colores_calipso, name='colores_calipso'),
]