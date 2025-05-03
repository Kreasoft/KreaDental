from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    web = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='empresa/logos/', blank=True, null=True)
    razon_social = models.CharField(max_length=200)
    representante_legal = models.CharField(max_length=200)
    fecha_inicio_licencia = models.DateField()
    fecha_fin_licencia = models.DateField()
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nombre 