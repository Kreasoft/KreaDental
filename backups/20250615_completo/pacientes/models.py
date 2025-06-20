from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from profesionales.models import Profesional
from prevision.models import Prevision
from empresa.models import Empresa

class Paciente(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombre = models.CharField(max_length=100,null=True,blank=True)
    apellidos = models.CharField(max_length=100,null=True,blank=True)
    documento = models.CharField(max_length=10, unique=True,null=True,blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES,null=True,blank=True)
    fecha_nacimiento = models.DateField(null=True,blank=True)
    telefono = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    direccion = models.TextField(null=True,blank=True)
    comuna = models.CharField(max_length=100,null=True,blank=True)
    ciudad = models.CharField(max_length=100,null=True,blank=True)    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    prevision = models.ForeignKey(Prevision, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Previsión')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='pacientes', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.apellidos:
            self.apellidos = self.apellidos.upper()
        if self.comuna:
            self.comuna = self.comuna.upper()
        if self.ciudad:
            self.ciudad = self.ciudad.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellidos', 'nombre'] 

class HistorialClinico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historiales_clinicos')
    fecha = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=50, choices=[
        ('consulta', 'Consulta'),
        ('examen', 'Examen'),
        ('tratamiento', 'Tratamiento'),
        ('otro', 'Otro')
    ])
    descripcion = models.TextField()
    observaciones = models.TextField(blank=True)
    profesional = models.ForeignKey(Profesional, on_delete=models.SET_NULL, null=True, blank=True)
    archivo = models.FileField(upload_to='historiales/', null=True, blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Historial Clínico'
        verbose_name_plural = 'Historiales Clínicos'

    def __str__(self):
        return f"{self.paciente} - {self.tipo} - {self.fecha}" 