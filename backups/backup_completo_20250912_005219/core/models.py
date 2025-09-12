from django.db import models
from django.conf import settings

class EmpresaModelo(models.Model):
    """
    Modelo abstracto que agrega relación con Empresa a otros modelos.
    """
    empresa = models.ForeignKey('empresa.Empresa', on_delete=models.CASCADE, editable=False)
    
    class Meta:
        abstract = True
