from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Empresa(models.Model):
    razon_social = models.CharField(max_length=100, verbose_name='Razón Social')
    nombre_fantasia = models.CharField(max_length=100, verbose_name='Nombre de Fantasía', null=True, blank=True)
    ruc = models.CharField(max_length=20, unique=True, verbose_name='RUT')
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    web = models.URLField(blank=True, null=True, verbose_name='Sitio Web')
    logo = models.ImageField(upload_to='empresas/logos/', blank=True, null=True)
    representante_legal = models.CharField(max_length=100)
    fecha_inicio_licencia = models.DateField()
    fecha_fin_licencia = models.DateField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre_fantasia']

    def __str__(self):
        return self.nombre_fantasia or self.razon_social

    def save(self, *args, **kwargs):
        if not self.nombre_fantasia:
            self.nombre_fantasia = self.razon_social
        super().save(*args, **kwargs)

class UsuarioEmpresa(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    es_administrador = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Usuario Empresa'
        verbose_name_plural = 'Usuarios Empresa'
        unique_together = ['usuario', 'empresa']

    def __str__(self):
        return f'{self.usuario.username} - {self.empresa.nombre_fantasia}'