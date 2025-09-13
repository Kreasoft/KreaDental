from django.contrib import admin
from .models import CierreCaja, RetiroCaja

@admin.register(CierreCaja)
class CierreCajaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'hora_apertura', 'estado', 'monto_inicial', 'total_retiros', 'saldo_final', 'usuario_apertura']
    list_filter = ['estado', 'fecha', 'usuario_apertura']
    search_fields = ['id', 'observaciones']
    readonly_fields = ['hora_apertura', 'saldo_final', 'total_retiros']
    ordering = ['-fecha', '-hora_apertura']

@admin.register(RetiroCaja)
class RetiroCajaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cierre_caja', 'concepto', 'monto', 'fecha_retiro', 'usuario_retiro']
    list_filter = ['fecha_retiro', 'usuario_retiro', 'cierre_caja__fecha']
    search_fields = ['concepto', 'comprobante', 'observaciones']
    readonly_fields = ['fecha_retiro']
    ordering = ['-fecha_retiro']
