from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from especialidades.models import Especialidad
from empresa.models import Empresa

# Obtener el modelo de usuario personalizado
User = get_user_model()

class Profesional(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    rut = models.CharField(max_length=12, unique=True, validators=[MinLengthValidator(9)], null=True, blank=True)
    nombres = models.CharField(max_length=100, default='')
    apellido_paterno = models.CharField(max_length=100, default='')
    apellido_materno = models.CharField(max_length=100, default='')
    fecha_nacimiento = models.DateField(default=timezone.now)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='M')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    direccion = models.TextField(blank=True, null=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True, blank=True, related_name='profesionales')
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='profesional_relacionado',
        verbose_name='usuario asociado'
    )
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='profesionales', null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombres']

    def __str__(self):
        return f"{self.nombre_completo()} - {self.rut}" if self.rut else self.nombre_completo()

    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}".strip()

    def get_especialidades(self):
        return self.especialidad.nombre if self.especialidad else ''

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper() if self.nombres else ''
        self.apellido_paterno = self.apellido_paterno.upper() if self.apellido_paterno else ''
        self.apellido_materno = self.apellido_materno.upper() if self.apellido_materno else ''
        super().save(*args, **kwargs) 