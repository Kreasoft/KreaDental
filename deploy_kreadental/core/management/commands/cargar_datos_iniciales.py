from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

class Command(BaseCommand):
    help = 'Carga datos iniciales para el sistema'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos iniciales...')
        
        try:
            with transaction.atomic():
                # Cargar empresa primero
                self.stdout.write('Cargando empresa...')
                call_command('loaddata', 'fixtures/empresa_inicial.json')
                
                # Cargar datos desde el fixture
                self.stdout.write('Cargando especialidades, profesionales y pacientes...')
                call_command('loaddata', 'datos_iniciales.json')
                
                self.stdout.write(self.style.SUCCESS('¡Datos cargados exitosamente!'))
                self.stdout.write('Se han cargado:')
                self.stdout.write('- 1 empresa')
                self.stdout.write('- 5 especialidades')
                self.stdout.write('- 3 profesionales')
                self.stdout.write('- 3 pacientes')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al cargar los datos: {str(e)}')) 