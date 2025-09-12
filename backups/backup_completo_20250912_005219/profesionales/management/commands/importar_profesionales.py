from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profesionales.models import Profesional
import json

class Command(BaseCommand):
    help = 'Importa los datos de los profesionales desde un archivo JSON'

    def handle(self, *args, **options):
        try:
            with open('profesionales_backup.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for prof_data in data:
                # Crear o actualizar usuario
                user_data = prof_data.pop('user', None)
                if user_data:
                    user, created = User.objects.get_or_create(
                        username=user_data['username'],
                        defaults={
                            'email': user_data['email'],
                            'first_name': user_data['first_name'],
                            'last_name': user_data['last_name']
                        }
                    )
                    if not created:
                        # Actualizar datos del usuario existente
                        user.email = user_data['email']
                        user.first_name = user_data['first_name']
                        user.last_name = user_data['last_name']
                        user.save()
                
                # Crear o actualizar profesional
                profesional, created = Profesional.objects.get_or_create(
                    documento=prof_data['documento'],
                    defaults={**prof_data, 'user': user}
                )
                
                if not created:
                    # Actualizar datos del profesional existente
                    for key, value in prof_data.items():
                        setattr(profesional, key, value)
                    profesional.user = user
                    profesional.save()
                
                status = 'creado' if created else 'actualizado'
                self.stdout.write(self.style.SUCCESS(
                    f'Profesional {profesional.nombre_completo()} {status} exitosamente'
                ))
                
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('No se encontró el archivo profesionales_backup.json'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al importar datos: {str(e)}')) 