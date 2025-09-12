from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from empresa.models import Empresa, Sucursal, UsuarioEmpresa

User = get_user_model()

class Command(BaseCommand):
    help = 'Asigna una sucursal al usuario especificado'

    def add_arguments(self, parser):
        parser.add_argument('email_usuario', type=str, help='Email del usuario')
        parser.add_argument('--empresa_id', type=int, help='ID de la empresa (opcional)')
        parser.add_argument('--sucursal_id', type=int, help='ID de la sucursal (opcional)')

    def handle(self, *args, **options):
        email_usuario = options['email_usuario']
        empresa_id = options.get('empresa_id')
        sucursal_id = options.get('sucursal_id')

        try:
            # Buscar el usuario por email
            usuario = User.objects.get(email=email_usuario)
            self.stdout.write(f"Usuario encontrado: {usuario.email}")

            # Si no se especifica empresa, usar la primera activa
            if empresa_id:
                empresa = Empresa.objects.get(id=empresa_id, activa=True)
            else:
                empresa = Empresa.objects.filter(activa=True).first()
            
            if not empresa:
                self.stdout.write(self.style.ERROR('No se encontró ninguna empresa activa'))
                return

            self.stdout.write(f"Empresa: {empresa.nombre_fantasia}")

            # Si no se especifica sucursal, usar la primera de la empresa
            if sucursal_id:
                sucursal = Sucursal.objects.get(id=sucursal_id, empresa=empresa, activa=True)
            else:
                sucursal = Sucursal.objects.filter(empresa=empresa, activa=True).first()

            if not sucursal:
                self.stdout.write(self.style.ERROR(f'No se encontró ninguna sucursal activa en {empresa.nombre_fantasia}'))
                return

            self.stdout.write(f"Sucursal: {sucursal.nombre}")

            # Crear o actualizar la relación UsuarioEmpresa
            usuario_empresa, created = UsuarioEmpresa.objects.get_or_create(
                usuario=usuario,
                empresa=empresa,
                defaults={
                    'sucursal': sucursal,
                    'tipo_usuario': 'admin_empresa',
                    'activo': True
                }
            )

            if not created:
                # Si ya existe, actualizar la sucursal
                usuario_empresa.sucursal = sucursal
                usuario_empresa.activo = True
                usuario_empresa.save()
                self.stdout.write(self.style.SUCCESS(f'Sucursal actualizada para {usuario.email}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Sucursal asignada exitosamente a {usuario.email}'))

            self.stdout.write(f"Usuario: {usuario.email}")
            self.stdout.write(f"Empresa: {empresa.nombre_fantasia}")
            self.stdout.write(f"Sucursal: {sucursal.nombre}")
            self.stdout.write(f"Tipo de usuario: {usuario_empresa.tipo_usuario}")

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario con email {email_usuario} no encontrado'))
        except Empresa.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Empresa con ID {empresa_id} no encontrada'))
        except Sucursal.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Sucursal con ID {sucursal_id} no encontrada'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 