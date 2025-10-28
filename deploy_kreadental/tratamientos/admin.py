from django.contrib import admin
from .models import Tratamiento, DetalleTratamiento

class DetalleTratamientoInline(admin.TabularInline):
    model = DetalleTratamiento
    extra = 0
    fields = ['procedimiento', 'profesional', 'cantidad', 'descuento', 'notas']

@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ['id', 'paciente', 'fecha_inicio', 'fecha_fin', 'estado', 'costo_total']
    list_filter = ['estado', 'fecha_inicio', 'fecha_fin']
    search_fields = ['paciente__nombre', 'paciente__apellidos', 'observaciones']
    date_hierarchy = 'fecha_inicio'
    inlines = [DetalleTratamientoInline]
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'costo_total']
    fieldsets = (
        ('Información General', {
            'fields': ('paciente', 'fecha_inicio', 'fecha_fin', 'estado', 'observaciones')
        }),
        ('Información de Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion', 'costo_total'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DetalleTratamiento)
class DetalleTratamientoAdmin(admin.ModelAdmin):
    list_display = ['tratamiento', 'procedimiento', 'profesional', 'cantidad', 'descuento']
    list_filter = ['procedimiento', 'profesional']
    search_fields = ['tratamiento__paciente__nombre', 'procedimiento__nombre', 'profesional__first_name']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

