from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
import os

User = get_user_model()

class Empresa(models.Model):
    razon_social = models.CharField(max_length=200)
    nombre_fantasia = models.CharField(max_length=200, blank=True, null=True)
    rut = models.CharField(max_length=20, unique=True, default="TEMP-RUT-00000000")
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    sitio_web = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_fantasia or self.razon_social

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

class Sucursal(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='sucursales')
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    horario_apertura = models.TimeField(blank=True, null=True)
    horario_cierre = models.TimeField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    es_principal = models.BooleanField(default=False, help_text="Indica si es la sucursal principal de la empresa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre_fantasia}"

    def save(self, *args, **kwargs):
        # Si esta sucursal es marcada como principal, desmarcar las otras
        if self.es_principal:
            Sucursal.objects.filter(empresa=self.empresa, es_principal=True).exclude(pk=self.pk).update(es_principal=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        unique_together = ['empresa', 'nombre']

class UsuarioEmpresa(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('super_admin', 'Super Administrador'),
        ('admin_empresa', 'Administrador Empresa'),
        ('admin_sucursal', 'Administrador Sucursal'),
        ('profesional', 'Profesional'),
        ('recepcion', 'Recepción'),
        ('auxiliar', 'Auxiliar'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='profesional')
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.empresa.nombre_fantasia}"

    class Meta:
        verbose_name = "Usuario Empresa"
        verbose_name_plural = "Usuarios Empresa"
        unique_together = ['usuario', 'empresa']

class PermisoUsuario(models.Model):
    usuario_empresa = models.ForeignKey(UsuarioEmpresa, on_delete=models.CASCADE, related_name='permisos')
    modulo = models.CharField(max_length=50, help_text="Nombre del módulo (ej: pacientes, citas, etc.)")
    puede_ver = models.BooleanField(default=True)
    puede_crear = models.BooleanField(default=False)
    puede_editar = models.BooleanField(default=False)
    puede_eliminar = models.BooleanField(default=False)
    puede_exportar = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario_empresa.usuario.username} - {self.modulo}"

    class Meta:
        verbose_name = "Permiso Usuario"
        verbose_name_plural = "Permisos Usuario"
        unique_together = ['usuario_empresa', 'modulo']