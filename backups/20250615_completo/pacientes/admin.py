from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'documento', 'genero', 'telefono', 'email')
    list_filter = ('fecha_registro', 'genero')
    search_fields = ('nombre', 'apellidos', 'documento')
    ordering = ('apellidos', 'nombre') 