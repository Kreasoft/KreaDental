from django.contrib import admin
from .models import PagoTratamiento, HistorialPago

@admin.register(PagoTratamiento)
class PagoTratamientoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tratamiento',
        'forma_pago',
        'monto',
        'fecha_pago',
        'estado',
        'creado_por'
    ]
    list_filter = ['estado', 'forma_pago', 'fecha_pago']
    search_fields = [
        'tratamiento__paciente__nombre',
        'tratamiento__paciente__apellidos',
        'comprobante'
    ]
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    ordering = ['-fecha_pago']

@admin.register(HistorialPago)
class HistorialPagoAdmin(admin.ModelAdmin):
    list_display = [
        'pago',
        'tipo_accion',
        'estado_anterior',
        'estado_nuevo',
        'monto_anterior',
        'monto_nuevo',
        'realizado_por',
        'fecha_accion'
    ]
    list_filter = ['tipo_accion', 'fecha_accion']
    search_fields = ['pago__id', 'notas']
    readonly_fields = ['fecha_accion']
    ordering = ['-fecha_accion']
