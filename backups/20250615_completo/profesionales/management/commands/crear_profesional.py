from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profesionales.models import Profesional, Especialidad

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un perfil de profesional para el usuario especificado'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario del profesional')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Verificar si ya tiene un perfil de profesional
            if hasattr(user, 'profesional'):
                self.stdout.write(self.style.WARNING(f'El usuario {username} ya tiene un perfil de profesional'))
                return
            
            # Crear una especialidad por defecto si no existe
            especialidad, created = Especialidad.objects.get_or_create(
                nombre='Odontología General',
                defaults={
                    'descripcion': 'Especialidad general en odontología',
                    'estado': 'ACTIVO'
                }
            )
            
            # Crear el perfil de profesional
            profesional = Profesional.objects.create(
                user=user,
                especialidad=especialidad,
                estado='ACTIVO'
            )
            
            self.stdout.write(self.style.SUCCESS(f'Se ha creado el perfil de profesional para {username}'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No se encontró el usuario {username}')) 