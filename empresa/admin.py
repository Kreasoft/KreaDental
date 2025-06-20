from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from .models import Empresa, Sucursal, UsuarioEmpresa, PermisoUsuario

# Personalizar el sitio de administración
admin_site = admin.AdminSite(name='admin')

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre_fantasia', 'razon_social', 'rut', 'telefono', 'email', 'activa', 'created_at']
    list_filter = ['activa', 'created_at']
    search_fields = ['nombre_fantasia', 'razon_social', 'rut', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('razon_social', 'nombre_fantasia', 'rut')
        }),
        ('Contacto', {
            'fields': ('direccion', 'telefono', 'email', 'sitio_web')
        }),
        ('Imagen', {
            'fields': ('logo',)
        }),
        ('Estado', {
            'fields': ('activa',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
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

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'telefono', 'email', 'es_principal', 'activa', 'created_at']
    list_filter = ['empresa', 'es_principal', 'activa', 'created_at']
    search_fields = ['nombre', 'empresa__nombre_fantasia', 'direccion', 'telefono']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('empresa', 'nombre')
        }),
        ('Contacto', {
            'fields': ('direccion', 'telefono', 'email')
        }),
        ('Horarios', {
            'fields': ('horario_apertura', 'horario_cierre')
        }),
        ('Estado', {
            'fields': ('activa', 'es_principal')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UsuarioEmpresa)
class UsuarioEmpresaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'empresa', 'sucursal', 'tipo_usuario', 'activo', 'fecha_inicio']
    list_filter = ['empresa', 'sucursal', 'tipo_usuario', 'activo', 'fecha_inicio']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'empresa__nombre_fantasia']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Usuario y Empresa', {
            'fields': ('usuario', 'empresa', 'sucursal')
        }),
        ('Rol y Estado', {
            'fields': ('tipo_usuario', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PermisoUsuario)
class PermisoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario_empresa', 'modulo', 'puede_ver', 'puede_crear', 'puede_editar', 'puede_eliminar']
    list_filter = ['modulo', 'puede_ver', 'puede_crear', 'puede_editar', 'puede_eliminar']
    search_fields = ['usuario_empresa__usuario__username', 'modulo']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Permisos', {
            'fields': ('usuario_empresa', 'modulo')
        }),
        ('Acciones Permitidas', {
            'fields': ('puede_ver', 'puede_crear', 'puede_editar', 'puede_eliminar', 'puede_exportar')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 