from django.core.management.base import BaseCommand
from especialidades.models import Especialidad
from profesionales.models import Profesional
from datetime import date

class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema'

    def handle(self, *args, **kwargs):
        # Crear especialidades
        esp1 = Especialidad.objects.create(
            nombre="Odontología General",
            descripcion="Servicios generales de odontología"
        )
        
        # Crear profesional
        Profesional.objects.create(
            rut="12345678-9",
            nombre="Juan",
            apellidos="Pérez",
            email="juan.perez@ejemplo.com",
            telefono="912345678",
            genero="M",
            fecha_nacimiento=date(1980, 1, 1),
            especialidad=esp1,
            activo=True
        )

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados exitosamente')) 