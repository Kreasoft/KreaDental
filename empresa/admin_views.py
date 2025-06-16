from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from .models import Empresa, UsuarioEmpresa

@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_empresa_inicial(request):
    try:
        # Crear la empresa
        empresa = Empresa.objects.create(
            razon_social="Mi Empresa",
            nombre_fantasia="Mi Empresa",
            ruc="11111111-1",
            representante_legal="Administrador",
            direccion="Dirección Principal",
            telefono="000000000",
            email="admin@example.com",
            activo=True
        )
        
        # Asignar al superusuario como administrador
        UsuarioEmpresa.objects.create(
            usuario=request.user,
            empresa=empresa,
            es_administrador=True,
            activo=True
        )
        
        # Guardar la empresa en la sesión
        request.session['empresa_id'] = empresa.id
        
        messages.success(request, 'Empresa creada y asignada exitosamente.')
        return redirect('core:home')
        
    except Exception as e:
        messages.error(request, f'Error al crear la empresa: {str(e)}')
        return redirect('admin:index') 