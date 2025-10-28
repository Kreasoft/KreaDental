from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from empresa.models import Empresa, UsuarioEmpresa

class Command(BaseCommand):
    help = 'Asigna permisos de administrador a un usuario para una empresa'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')
        parser.add_argument('empresa_id', type=int, help='ID de la empresa')

    def handle(self, *args, **options):
        username = options['username']
        empresa_id = options['empresa_id']

        try:
            usuario = User.objects.get(username=username)
            empresa = Empresa.objects.get(id=empresa_id)
            
            # Crear o actualizar el UsuarioEmpresa
            usuario_empresa, created = UsuarioEmpresa.objects.get_or_create(
                usuario=usuario,
                empresa=empresa,
                defaults={
                    'tipo_usuario': 'admin_empresa',
                    'activo': True
                }
            )
            
            if not created:
                usuario_empresa.tipo_usuario = 'admin_empresa'
                usuario_empresa.activo = True
                usuario_empresa.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuario {username} asignado como administrador de {empresa.nombre_fantasia}'
                )
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuario {username} no encontrado')
            )
        except Empresa.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Empresa con ID {empresa_id} no encontrada')
            ) 