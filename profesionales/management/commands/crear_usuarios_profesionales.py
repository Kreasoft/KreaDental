from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profesionales.models import Profesional

class Command(BaseCommand):
    help = 'Crea usuarios para los profesionales que no tienen uno asociado'

    def handle(self, *args, **options):
        profesionales_sin_usuario = Profesional.objects.filter(user__isnull=True)
        
        for profesional in profesionales_sin_usuario:
            # Crear nombre de usuario basado en el documento
            username = f"prof_{profesional.documento}"
            
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'Usuario {username} ya existe'))
                continue
            
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=profesional.email,
                password=profesional.documento,  # Usar el documento como contraseña inicial
                first_name=profesional.nombre,
                last_name=profesional.apellidos
            )
            
            # Asociar el usuario al profesional
            profesional.user = user
            profesional.save()
            
            self.stdout.write(self.style.SUCCESS(f'Usuario creado para {profesional.nombre_completo()}')) 