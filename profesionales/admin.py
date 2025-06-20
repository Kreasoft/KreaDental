from django.contrib import admin
from .models import Profesional

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'rut', 'email', 'especialidad', 'empresa', 'activo', 'es_compartido', 'compartir_entre_sucursales']
    list_filter = ['activo', 'genero', 'especialidad', 'empresa', 'compartir_entre_sucursales', 'fecha_creacion']
    search_fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'rut', 'email']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    filter_horizontal = ['empresas_compartidas']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'genero')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Información Profesional', {
            'fields': ('especialidad', 'activo')
        }),
        ('Empresa', {
            'fields': ('empresa',)
        }),
        ('Compartición entre Sucursales', {
            'fields': ('compartir_entre_sucursales', 'empresas_compartidas'),
            'description': 'Configuración para compartir este profesional con otras sucursales'
        }),
        ('Usuario del Sistema', {
            'fields': ('usuario',),
            'description': 'Usuario asociado para acceso al sistema'
        }),
    )
    
    def get_citas(self, obj):
        return obj.citas_profesional.count()
    get_citas.short_description = 'Total Citas'

    def get_especialidades(self, obj):
        return obj.especialidad.nombre if obj.especialidad else ''
    get_especialidades.short_description = 'Especialidad' 