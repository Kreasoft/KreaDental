from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
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
    
    # Campos para compartición entre sucursales
    compartir_entre_sucursales = models.BooleanField(
        default=False, 
        verbose_name='Compartir con otras sucursales',
        help_text='Permite que otras sucursales vean este profesional'
    )
    empresas_compartidas = models.ManyToManyField(
        Empresa, 
        blank=True, 
        related_name='profesionales_compartidos',
        verbose_name='Sucursales con acceso',
        help_text='Selecciona las sucursales que pueden ver este profesional'
    )
    
    # Campo para porcentaje de utilidad de procedimientos
    porcentaje_utilidad = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[
            MinValueValidator(0.00, message='El porcentaje debe ser mayor o igual a 0'),
            MaxValueValidator(100.00, message='El porcentaje debe ser menor o igual a 100')
        ],
        verbose_name='Porcentaje de Utilidad',
        help_text='Porcentaje de utilidad que recibe el profesional por procedimientos realizados (0.00 - 100.00)'
    )

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

    def es_compartido(self):
        """Verifica si el profesional está compartido con otras sucursales"""
        return self.compartir_entre_sucursales and self.empresas_compartidas.exists()

    def puede_ver_empresa(self, empresa):
        """Verifica si una empresa puede ver este profesional"""
        if self.empresa == empresa:
            return True
        return self.compartir_entre_sucursales and empresa in self.empresas_compartidas.all()

    def calcular_utilidad_procedimiento(self, costo_procedimiento):
        """
        Calcula la utilidad que le corresponde al profesional por un procedimiento
        """
        if not self.porcentaje_utilidad or costo_procedimiento <= 0:
            return 0
        return (costo_procedimiento * self.porcentaje_utilidad) / 100

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper() if self.nombres else ''
        self.apellido_paterno = self.apellido_paterno.upper() if self.apellido_paterno else ''
        self.apellido_materno = self.apellido_materno.upper() if self.apellido_materno else ''
        super().save(*args, **kwargs) 