from django.contrib import admin
from .models import Paciente, HistorialClinico

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'documento', 'email', 'telefono', 'empresa', 'activo', 'es_compartido', 'compartir_entre_sucursales']
    list_filter = ['activo', 'genero', 'empresa', 'compartir_entre_sucursales', 'fecha_registro']
    search_fields = ['nombre', 'apellidos', 'documento', 'email']
    readonly_fields = ['fecha_registro']
    filter_horizontal = ['empresas_compartidas']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellidos', 'documento', 'genero', 'fecha_nacimiento')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion', 'comuna', 'ciudad')
        }),
        ('Información Clínica', {
            'fields': ('prevision', 'activo')
        }),
        ('Empresa', {
            'fields': ('empresa',)
        }),
        ('Compartición entre Sucursales', {
            'fields': ('compartir_entre_sucursales', 'empresas_compartidas'),
            'description': 'Configuración para compartir este paciente con otras sucursales'
        }),
    )

@admin.register(HistorialClinico)
class HistorialClinicoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'tipo', 'fecha', 'profesional']
    list_filter = ['tipo', 'fecha', 'profesional']
    search_fields = ['paciente__nombre', 'paciente__apellidos', 'descripcion']
    readonly_fields = ['fecha'] 