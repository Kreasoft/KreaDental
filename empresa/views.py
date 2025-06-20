from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden, JsonResponse
from .models import Empresa, UsuarioEmpresa, Sucursal
from .forms import EmpresaForm, SucursalForm, UsuarioEmpresaForm
from datetime import date, timedelta

@login_required
def seleccionar_empresa(request):
    # Obtener las empresas del usuario
    empresas = Empresa.objects.filter(
        usuarioempresa__usuario=request.user,
        usuarioempresa__activo=True
    ).distinct()
    
    return render(request, 'empresa/seleccionar_empresa.html', {
        'empresas': empresas
    })

@login_required
def cambiar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    # Verificar que el usuario tenga acceso a esta empresa
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        activo=True
    ).exists():
        messages.error(request, 'No tienes acceso a esta empresa.')
        return redirect('empresa:seleccionar_empresa')
    
    # Guardar la empresa seleccionada en la sesión
    request.session['empresa_actual_id'] = empresa.id
    messages.success(request, f'Has cambiado a la empresa: {empresa.nombre_fantasia}')
    
    return redirect('core:home')

@login_required
def editar_empresa(request, empresa_id=None):
    """Vista para editar o crear una empresa."""
    # Verificar si el usuario es administrador de la empresa
    if empresa_id:
        empresa = get_object_or_404(Empresa, id=empresa_id, activa=True)
        if not UsuarioEmpresa.objects.filter(
            usuario=request.user, 
            empresa=empresa, 
            tipo_usuario__in=['super_admin', 'admin_empresa']
        ).exists():
            return HttpResponseForbidden("No tienes permiso para editar esta empresa")
    else:
        empresa = None
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.save()
            
            # Si es una nueva empresa, asignar al usuario actual como administrador
            if not empresa_id:
                UsuarioEmpresa.objects.create(
                    usuario=request.user,
                    empresa=empresa,
                    tipo_usuario='admin_empresa'
                )
                request.session['empresa_actual_id'] = str(empresa.id)
            
            messages.success(request, 'Empresa guardada correctamente.')
            return redirect('empresa:editar_empresa', empresa_id=empresa.id)
    else:
        form = EmpresaForm(instance=empresa)
    
    return render(request, 'empresa/form_empresa.html', {
        'form': form,
        'empresa': empresa
    })

@login_required
def listar_empresas(request):
    # Obtener empresas del usuario
    empresas = Empresa.objects.filter(
        usuarioempresa__usuario=request.user,
        usuarioempresa__activo=True
    ).distinct()
    
    return render(request, 'empresa/listar_empresas.html', {
        'empresas': empresas
    })

@login_required
def desactivar_empresa(request, empresa_id):
    """Desactiva una empresa (borrado lógico)."""
    empresa = get_object_or_404(Empresa, id=empresa_id, activa=True)
    
    # Verificar que el usuario sea administrador de la empresa
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user, 
        empresa=empresa, 
        tipo_usuario__in=['super_admin', 'admin_empresa']
    ).exists():
        return HttpResponseForbidden("No tienes permiso para desactivar esta empresa")
    
    # No permitir desactivar si es la única empresa del usuario
    if UsuarioEmpresa.objects.filter(usuario=request.user).count() <= 1:
        messages.error(request, 'No puedes desactivar tu única empresa')
        return redirect('empresa:listar_empresas')
    
    # Si la empresa actual es la que se va a desactivar, cambiar a otra empresa
    if str(empresa.id) == request.session.get('empresa_actual_id'):
        otra_empresa = Empresa.objects.filter(
            usuarioempresa__usuario=request.user,
            activa=True
        ).exclude(id=empresa.id).first()
        
        if otra_empresa:
            request.session['empresa_actual_id'] = str(otra_empresa.id)
    
    # Desactivar la empresa
    empresa.activa = False
    empresa.save()
    
    messages.success(request, f'Empresa {empresa.nombre_fantasia or empresa.razon_social} desactivada correctamente')
    return redirect('empresa:listar_empresas')

@login_required
def crear_empresa_inicial(request):
    if request.method == 'POST':
        try:
            # Crear la empresa
            empresa = Empresa.objects.create(
                razon_social=request.POST.get('razon_social'),
                nombre_fantasia=request.POST.get('nombre_fantasia'),
                rut=request.POST.get('rut'),
                direccion=request.POST.get('direccion'),
                telefono=request.POST.get('telefono'),
                email=request.POST.get('email'),
                sitio_web=request.POST.get('sitio_web'),
                activa=True
            )
            
            # Asignar el usuario como administrador de la empresa
            UsuarioEmpresa.objects.create(
                usuario=request.user,
                empresa=empresa,
                tipo_usuario='admin_empresa',
                activo=True
            )
            
            # Establecer la empresa en la sesión
            request.session['empresa_id'] = str(empresa.id)
            
            messages.success(request, 'Empresa creada exitosamente.')
            return redirect('core:home')
            
        except Exception as e:
            messages.error(request, f'Error al crear la empresa: {str(e)}')
    
    return render(request, 'empresa/crear_empresa_inicial.html')

@login_required
def configuracion_empresa(request):
    """Vista para la configuración detallada de la empresa."""
    empresa = get_object_or_404(Empresa, id=request.session.get('empresa_id'), activa=True)
    
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user, 
        empresa=empresa, 
        tipo_usuario__in=['super_admin', 'admin_empresa']
    ).exists():
        return HttpResponseForbidden("No tienes permiso para configurar esta empresa")
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            empresa = form.save()
            messages.success(request, 'Configuración de empresa actualizada correctamente.')
            return redirect('empresa:configuracion_empresa')
    else:
        form = EmpresaForm(instance=empresa)
    
    return render(request, 'empresa/configuracion_empresa.html', {
        'form': form,
        'empresa': empresa
    })

@login_required
def eliminar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    # Verificar permisos
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        tipo_usuario__in=['super_admin', 'admin_empresa'],
        activo=True
    ).exists():
        messages.error(request, 'No tienes permisos para eliminar esta empresa.')
        return redirect('empresa:listar_empresas')
    
    if request.method == 'POST':
        empresa.activa = False
        empresa.save()
        messages.success(request, 'Empresa desactivada exitosamente.')
        return redirect('empresa:listar_empresas')
    
    return render(request, 'empresa/confirmar_eliminar.html', {
        'empresa': empresa
    })

# Vistas para Sucursales
@login_required
def listar_sucursales(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    # Verificar permisos
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        activo=True
    ).exists():
        messages.error(request, 'No tienes acceso a esta empresa.')
        return redirect('empresa:seleccionar_empresa')
    
    sucursales = Sucursal.objects.filter(empresa=empresa)
    
    return render(request, 'empresa/lista_sucursales.html', {
        'empresa': empresa,
        'sucursales': sucursales
    })

@login_required
def crear_sucursal(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    # Verificar permisos
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        tipo_usuario__in=['super_admin', 'admin_empresa'],
        activo=True
    ).exists():
        messages.error(request, 'No tienes permisos para crear sucursales.')
        return redirect('empresa:listar_sucursales', empresa_id=empresa_id)
    
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            sucursal = form.save(commit=False)
            sucursal.empresa = empresa
            sucursal.save()
            messages.success(request, 'Sucursal creada exitosamente.')
            return redirect('empresa:listar_sucursales', empresa_id=empresa_id)
    else:
        form = SucursalForm()
    
    return render(request, 'empresa/form_sucursal.html', {
        'form': form,
        'empresa': empresa,
        'titulo': 'Crear Nueva Sucursal'
    })

@login_required
def editar_sucursal(request, empresa_id, sucursal_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, empresa=empresa)
    
    # Verificar permisos
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        tipo_usuario__in=['super_admin', 'admin_empresa'],
        activo=True
    ).exists():
        messages.error(request, 'No tienes permisos para editar sucursales.')
        return redirect('empresa:listar_sucursales', empresa_id=empresa_id)
    
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucursal actualizada exitosamente.')
            return redirect('empresa:listar_sucursales', empresa_id=empresa_id)
    else:
        form = SucursalForm(instance=sucursal)
    
    return render(request, 'empresa/form_sucursal.html', {
        'form': form,
        'empresa': empresa,
        'sucursal': sucursal,
        'titulo': 'Editar Sucursal'
    })

@login_required
def eliminar_sucursal(request, empresa_id, sucursal_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, empresa=empresa)
    
    # Verificar permisos
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        tipo_usuario__in=['super_admin', 'admin_empresa'],
        activo=True
    ).exists():
        messages.error(request, 'No tienes permisos para eliminar sucursales.')
        return redirect('empresa:listar_sucursales', empresa_id=empresa_id)
    
    if request.method == 'POST':
        sucursal.activa = False
        sucursal.save()
        messages.success(request, 'Sucursal desactivada exitosamente.')
        return redirect('empresa:listar_sucursales', empresa_id=empresa_id)
    
    return render(request, 'empresa/confirmar_eliminar_sucursal.html', {
        'empresa': empresa,
        'sucursal': sucursal
    })

@login_required
def listar_usuarios_empresa(request, empresa_id):
    """Lista todos los usuarios de una empresa específica"""
    empresa = get_object_or_404(Empresa, id=empresa_id, activa=True)
    
    # Verificar permisos del usuario actual
    usuario_actual = UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        activo=True
    ).first()
    
    if not usuario_actual:
        messages.error(request, 'No tienes permisos para ver usuarios de esta empresa.')
        return redirect('empresa:listar_empresas')
    
    # Solo super_admin y admin_empresa pueden ver usuarios
    if usuario_actual.tipo_usuario not in ['super_admin', 'admin_empresa']:
        messages.error(request, 'No tienes permisos para gestionar usuarios.')
        return redirect('empresa:listar_empresas')
    
    usuarios = UsuarioEmpresa.objects.filter(empresa=empresa).select_related('usuario', 'sucursal')
    
    context = {
        'empresa': empresa,
        'usuarios': usuarios,
        'usuario_actual': usuario_actual,
    }
    
    return render(request, 'empresa/lista_usuarios.html', context)

@login_required
def crear_usuario_empresa(request, empresa_id):
    """Crea un nuevo usuario para una empresa"""
    empresa = get_object_or_404(Empresa, id=empresa_id, activa=True)
    
    # Verificar permisos del usuario actual
    usuario_actual = UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        activo=True
    ).first()
    
    if not usuario_actual:
        return JsonResponse({
            'success': False,
            'message': 'No tienes permisos para crear usuarios en esta empresa.'
        })
    
    # Solo super_admin y admin_empresa pueden crear usuarios
    if usuario_actual.tipo_usuario not in ['super_admin', 'admin_empresa']:
        return JsonResponse({
            'success': False,
            'message': 'No tienes permisos para crear usuarios.'
        })
    
    if request.method == 'POST':
        form = UsuarioEmpresaForm(request.POST, empresa=empresa, usuario_actual=usuario_actual)
        if form.is_valid():
            usuario_empresa = form.save(commit=False)
            usuario_empresa.empresa = empresa
            usuario_empresa.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Usuario {usuario_empresa.usuario.email} creado exitosamente.',
                'redirect_url': reverse('empresa:listar_usuarios_empresa', args=[empresa.id])
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Por favor corrige los errores en el formulario.',
                'errors': form.errors
            })
    else:
        form = UsuarioEmpresaForm(empresa=empresa, usuario_actual=usuario_actual)
    
    context = {
        'form': form,
        'empresa': empresa,
        'titulo': 'Crear Usuario',
    }
    
    return render(request, 'empresa/form_usuario_empresa.html', context)

@login_required
def editar_usuario_empresa(request, empresa_id, usuario_empresa_id):
    """Edita un usuario de empresa existente"""
    empresa = get_object_or_404(Empresa, id=empresa_id, activa=True)
    usuario_empresa = get_object_or_404(UsuarioEmpresa, id=usuario_empresa_id, empresa=empresa)
    
    # Verificar permisos del usuario actual
    usuario_actual = UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        activo=True
    ).first()
    
    if not usuario_actual:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'No tienes permisos para editar usuarios de esta empresa.'
            })
        messages.error(request, 'No tienes permisos para editar usuarios de esta empresa.')
        return redirect('empresa:listar_empresas')
    
    # Solo super_admin y admin_empresa pueden editar usuarios
    if usuario_actual.tipo_usuario not in ['super_admin', 'admin_empresa']:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'No tienes permisos para editar usuarios.'
            })
        messages.error(request, 'No tienes permisos para editar usuarios.')
        return redirect('empresa:listar_empresas')
    
    # Un usuario no puede editarse a sí mismo
    if usuario_empresa.usuario == request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'No puedes editar tu propio perfil desde aquí.'
            })
        messages.error(request, 'No puedes editar tu propio perfil desde aquí.')
        return redirect('empresa:listar_usuarios_empresa', empresa_id=empresa.id)
    
    if request.method == 'POST':
        form = UsuarioEmpresaForm(request.POST, instance=usuario_empresa, empresa=empresa, usuario_actual=usuario_actual)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Usuario {usuario_empresa.usuario.email} actualizado exitosamente.',
                    'redirect_url': reverse('empresa:listar_usuarios_empresa', args=[empresa.id])
                })
            messages.success(request, f'Usuario {usuario_empresa.usuario.email} actualizado exitosamente.')
            return redirect('empresa:listar_usuarios_empresa', empresa_id=empresa.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Por favor corrige los errores en el formulario.',
                    'errors': form.errors
                })
    else:
        form = UsuarioEmpresaForm(instance=usuario_empresa, empresa=empresa, usuario_actual=usuario_actual)
    
    context = {
        'form': form,
        'empresa': empresa,
        'usuario_empresa': usuario_empresa,
        'titulo': 'Editar Usuario',
    }
    
    return render(request, 'empresa/form_usuario_empresa.html', context)

@login_required
def eliminar_usuario_empresa(request, empresa_id, usuario_empresa_id):
    """Desactiva un usuario de empresa"""
    empresa = get_object_or_404(Empresa, id=empresa_id, activa=True)
    usuario_empresa = get_object_or_404(UsuarioEmpresa, id=usuario_empresa_id, empresa=empresa)
    
    # Verificar permisos del usuario actual
    usuario_actual = UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=empresa,
        activo=True
    ).first()
    
    if not usuario_actual:
        messages.error(request, 'No tienes permisos para eliminar usuarios de esta empresa.')
        return redirect('empresa:listar_empresas')
    
    # Solo super_admin y admin_empresa pueden eliminar usuarios
    if usuario_actual.tipo_usuario not in ['super_admin', 'admin_empresa']:
        messages.error(request, 'No tienes permisos para eliminar usuarios.')
        return redirect('empresa:listar_empresas')
    
    # Un usuario no puede eliminarse a sí mismo
    if usuario_empresa.usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propio perfil.')
        return redirect('empresa:listar_usuarios_empresa', empresa_id=empresa.id)
    
    if request.method == 'POST':
        usuario_empresa.activo = False
        usuario_empresa.save()
        messages.success(request, f'Usuario {usuario_empresa.usuario.email} desactivado exitosamente.')
        return redirect('empresa:listar_usuarios_empresa', empresa_id=empresa.id)
    
    context = {
        'empresa': empresa,
        'usuario_empresa': usuario_empresa,
    }
    
    return render(request, 'empresa/confirmar_eliminar_usuario.html', context)

@login_required
def cambiar_sucursal(request, sucursal_id):
    """Cambia la sucursal actual del usuario"""
    from .models import Sucursal, UsuarioEmpresa
    
    # Verificar que el usuario tenga acceso a esta sucursal
    sucursal = get_object_or_404(Sucursal, id=sucursal_id, activa=True)
    
    # Verificar que el usuario tenga acceso a la empresa de esta sucursal
    usuario_empresa = UsuarioEmpresa.objects.filter(
        usuario=request.user,
        empresa=sucursal.empresa,
        activo=True
    ).first()
    
    if not usuario_empresa:
        messages.error(request, 'No tienes acceso a esta sucursal.')
        return redirect('core:home')
    
    # Actualizar la sucursal del usuario
    usuario_empresa.sucursal = sucursal
    usuario_empresa.save()
    
    # Guardar la empresa en la sesión si no está
    if 'empresa_actual_id' not in request.session:
        request.session['empresa_actual_id'] = sucursal.empresa.id
    
    messages.success(request, f'Has cambiado a la sucursal: {sucursal.nombre}')
    return redirect('core:home')