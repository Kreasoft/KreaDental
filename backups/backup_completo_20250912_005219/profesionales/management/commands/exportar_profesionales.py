from django.core.management.base import BaseCommand
from django.core import serializers
from profesionales.models import Profesional
import json

class Command(BaseCommand):
    help = 'Exporta los datos de los profesionales a un archivo JSON'

    def handle(self, *args, **options):
        profesionales = Profesional.objects.all()
        data = []
        
        for profesional in profesionales:
            prof_data = {
                'nombre': profesional.nombre,
                'nombres': profesional.nombres,
                'apellido_paterno': profesional.apellido_paterno,
                'apellido_materno': profesional.apellido_materno,
                'documento': profesional.documento,
                'especialidad': profesional.especialidad,
                'telefono': profesional.telefono,
                'email': profesional.email,
                'direccion': profesional.direccion,
                'comuna': profesional.comuna,
                'ciudad': profesional.ciudad,
                'activo': profesional.activo,
                'user': {
                    'username': profesional.user.username,
                    'email': profesional.user.email,
                    'first_name': profesional.user.first_name,
                    'last_name': profesional.user.last_name,
                } if profesional.user else None
            }
            data.append(prof_data)
        
        with open('profesionales_backup.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        self.stdout.write(self.style.SUCCESS(f'Se exportaron {len(data)} profesionales')) 