from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Obtener el modelo de usuario personalizado
User = get_user_model()

class ConfiguracionEmpresa(models.Model):
    nombre = models.CharField('Nombre de la Empresa', max_length=200)
    rut = models.CharField('RUT', max_length=12)
    direccion = models.TextField('Dirección')
    telefono = models.CharField('Teléfono', max_length=20)
    email = models.EmailField('Email')
    sitio_web = models.URLField('Sitio Web', blank=True, null=True)
    logo = models.ImageField(
        upload_to='logos/',
        null=True,
        blank=True,
        verbose_name='Logo de la empresa',
        help_text='Sube una imagen en formato PNG o JPG (tamaño recomendado: 200x200 píxeles)')
    horario_atencion = models.TextField('Horario de Atención', blank=True)
    descripcion = models.TextField('Descripción', blank=True)
    terminos_condiciones = models.TextField('Términos y Condiciones', blank=True)
    politica_privacidad = models.TextField('Política de Privacidad', blank=True)
    redes_sociales = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        verbose_name='Redes Sociales',
        help_text='Ingresa las URLs de tus redes sociales')
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última Actualización', auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Configuración de Empresa'
        verbose_name_plural = 'Configuración de Empresa'


class PreferenciaUsuario(models.Model):
    FUENTES_DISPONIBLES = [
        ('Poppins', 'Poppins'),
        ('Inter', 'Inter'),
        ('Outfit', 'Outfit'),
        ('Plus Jakarta Sans', 'Plus Jakarta Sans'),
        ('DM Sans', 'DM Sans'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferencias',
        verbose_name='usuario'
    )
    fuente = models.CharField(
        'Fuente del Sistema',
        max_length=50,
        choices=FUENTES_DISPONIBLES,
        default='Plus Jakarta Sans'
    )
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última Actualización', auto_now=True)

    def __str__(self):
        return f'Preferencias de {self.usuario.username}'

    class Meta:
        verbose_name = 'Preferencia de Usuario'
        verbose_name_plural = 'Preferencias de Usuarios'

