from django.core.management.base import BaseCommand
from usuarios.models import Usuario
from empresa.models import Empresa, UsuarioEmpresa

class Command(BaseCommand):
    help = 'Asigna permisos de administrador a Ricardo González Gaete'

    def handle(self, *args, **options):
        try:
            # Buscar el usuario por email
            usuario = Usuario.objects.get(email='kreasoft@gmail.com')
            self.stdout.write(f'Usuario encontrado: {usuario.first_name} {usuario.last_name}')
            
            # Buscar la empresa
            empresa = Empresa.objects.get(id=1)
            self.stdout.write(f'Empresa encontrada: {empresa.nombre_fantasia}')
            
            # Crear o actualizar el UsuarioEmpresa
            usuario_empresa, created = UsuarioEmpresa.objects.get_or_create(
                usuario=usuario, 
                empresa=empresa, 
                defaults={
                    'tipo_usuario': 'admin_empresa',
                    'activo': True
                }
            )
            
            # Asegurar que tenga los permisos correctos
            usuario_empresa.tipo_usuario = 'admin_empresa'
            usuario_empresa.activo = True
            usuario_empresa.save()
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS('✅ Permiso de admin_empresa creado y asignado correctamente.')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('✅ Permiso de admin_empresa actualizado correctamente.')
                )
                
        except Usuario.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Error: No se encontró el usuario con email kreasoft@gmail.com')
            )
        except Empresa.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Error: No se encontró la empresa con ID 1')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error inesperado: {str(e)}')
            ) 