from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.conf import settings


class UsuarioManager(BaseUserManager):
    """Define un administrador de modelo para el modelo Usuario sin el campo 'username'."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Crea y guarda un usuario con el email y contraseña dados."""
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario regular con el email y contraseña dados."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Crea y guarda un superusuario con el email y contraseña dados."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """Modelo de usuario personalizado que usa email en lugar de username."""
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    telefono = models.CharField(_('teléfono'), max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField(_('dirección'), blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    pais = models.CharField(_('país'), max_length=100, blank=True)
    codigo_postal = models.CharField(_('código postal'), max_length=20, blank=True)
    
    # Relación con empresas a través del modelo UsuarioEmpresa
    # El related_name 'empresas_relacionadas' debe coincidir con el definido en UsuarioEmpresa
    empresas = models.ManyToManyField(
        'empresa.Empresa',
        through='empresa.UsuarioEmpresa',
        related_name='usuarios',  # Este es el related_name que se usará para acceder desde Empresa
        blank=True,
        verbose_name='empresas'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Eliminamos 'email' de REQUIRED_FIELDS
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return self.get_full_name() or self.email
    
    def get_short_name(self):
        """Devuelve el nombre corto del usuario (nombre)."""
        return self.first_name
    
    def get_full_name(self):
        """
        Devuelve el nombre completo del usuario.
        """
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.email
    
    @property
    def nombre_completo(self):
        """Propiedad para acceder al nombre completo."""
        return self.get_full_name()
    
    @property
    def iniciales(self):
        """Devuelve las iniciales del usuario."""
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.first_name:
            return self.first_name[0].upper()
        elif self.email:
            return self.email[0].upper()
        return '?'
