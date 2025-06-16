from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from .models import Empresa, UsuarioEmpresa

# Personalizar el sitio de administración
admin_site = admin.AdminSite(name='admin')

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'nombre_fantasia', 'ruc', 'email', 'telefono', 'activo')
    search_fields = ('razon_social', 'nombre_fantasia', 'ruc')
    list_filter = ('activo',)
    ordering = ('razon_social',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('razon_social', 'nombre_fantasia', 'ruc', 'email', 'telefono', 'web')
        }),
        ('Dirección', {
            'fields': ('direccion',)
        }),
        ('Información Legal', {
            'fields': ('representante_legal', 'fecha_inicio_licencia', 'fecha_fin_licencia')
        }),
        ('Configuración', {
            'fields': ('logo', 'activo', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('crear-empresa-inicial/', self.admin_site.admin_view(self.crear_empresa_inicial), name='crear_empresa_inicial'),
        ]
        return custom_urls + urls

    def crear_empresa_inicial(self, request, queryset):
        url = reverse('empresa:crear_empresa_inicial_superusuario')
        return redirect(url)
    crear_empresa_inicial.short_description = 'Crear Empresa Inicial'

    class Media:
        css = {
            'all': ('admin/css/empresa_admin.css',)
        }

@admin.register(UsuarioEmpresa)
class UsuarioEmpresaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'empresa', 'es_administrador', 'activo')
    list_filter = ('es_administrador', 'activo', 'empresa')
    search_fields = ('usuario__username', 'empresa__razon_social')
    ordering = ('empresa', 'usuario')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Información de Usuario', {
            'fields': ('usuario', 'empresa', 'es_administrador')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_creacion', 'fecha_actualizacion')
        }),
    ) 