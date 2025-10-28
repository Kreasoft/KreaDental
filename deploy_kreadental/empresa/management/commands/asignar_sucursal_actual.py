from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from empresa.models import Empresa, Sucursal, UsuarioEmpresa

User = get_user_model()

class Command(BaseCommand):
    help = 'Asigna automáticamente la primera sucursal disponible al usuario actual'

    def handle(self, *args, **options):
        try:
            # Obtener el primer usuario (asumiendo que es el usuario actual)
            usuario = User.objects.first()
            if not usuario:
                self.stdout.write(self.style.ERROR('No se encontró ningún usuario'))
                return

            self.stdout.write(f"Usuario: {usuario.email}")

            # Obtener la primera empresa activa
            empresa = Empresa.objects.filter(activa=True).first()
            if not empresa:
                self.stdout.write(self.style.ERROR('No se encontró ninguna empresa activa'))
                return

            self.stdout.write(f"Empresa: {empresa.nombre_fantasia}")

            # Obtener la primera sucursal activa de la empresa
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

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 