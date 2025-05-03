from django.db import models
from especialidades.models import Especialidad

class Procedimiento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tiempo_estimado = models.IntegerField(help_text="Tiempo estimado en minutos", default=30)
    estado = models.BooleanField(default=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, related_name='procedimientos', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Procedimiento'
        verbose_name_plural = 'Procedimientos'
        ordering = ['nombre'] 