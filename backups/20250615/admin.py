from django.contrib import admin
from .models import Profesional

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellido_paterno', 'apellido_materno', 'rut', 'especialidad', 'telefono', 'email', 'activo')
    search_fields = ('nombres', 'apellido_paterno', 'apellido_materno', 'rut')
    ordering = ('apellido_paterno', 'apellido_materno', 'nombres')
    list_filter = ('activo', 'genero', 'especialidad')
    fieldsets = (
        ('Información Personal', {
            'fields': ('rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'genero')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Información Profesional', {
            'fields': ('especialidad', 'usuario', 'activo')
        }),
    )
    
    def get_citas(self, obj):
        return obj.citas_profesional.count()
    get_citas.short_description = 'Total Citas'

    def get_especialidades(self, obj):
        return obj.especialidad.nombre if obj.especialidad else ''
    get_especialidades.short_description = 'Especialidad' 