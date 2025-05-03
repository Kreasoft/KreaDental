from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'hora', 'paciente', 'profesional', 'estado']
    list_filter = ['fecha', 'estado', 'profesional']
    search_fields = ['paciente__nombre', 'profesional__nombre', 'motivo']
    date_hierarchy = 'fecha' 