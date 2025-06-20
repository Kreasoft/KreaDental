from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import Empresa, UsuarioEmpresa
from .forms import EmpresaForm
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
    # Verificar que el usuario tenga permiso para acceder a esta empresa
    if UsuarioEmpresa.objects.filter(usuario=request.user, empresa=empresa, activo=True).exists():
        request.session['empresa_id'] = str(empresa.id)
        messages.success(request, f'Has seleccionado la empresa: {empresa.nombre_fantasia|default:empresa.razon_social}')
        return redirect('core:home')
    else:
        messages.error(request, 'No tienes permiso para acceder a esta empresa.')
        return redirect('empresa:seleccionar_empresa')

@login_required
def editar_empresa(request, empresa_id=None):
    """Vista para editar o crear una empresa."""
    # Verificar si el usuario es administrador de la empresa
    if empresa_id:
        empresa = get_object_or_404(Empresa, id=empresa_id, activo=True)
        if not UsuarioEmpresa.objects.filter(
            usuario=request.user, 
            empresa=empresa, 
            es_administrador=True
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
                    es_administrador=True
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
    # Obtener las empresas del usuario
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
    empresa = get_object_or_404(Empresa, id=empresa_id, activo=True)
    
    # Verificar que el usuario sea administrador de la empresa
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user, 
        empresa=empresa, 
        es_administrador=True
    ).exists():
        return HttpResponseForbidden("No tienes permiso para desactivar esta empresa")
    
    # No permitir desactivar si es la única empresa del usuario
    if UsuarioEmpresa.objects.filter(usuario=request.user).count() <= 1:
        messages.error(request, 'No puedes desactivar tu única empresa')
        return redirect('empresa:listar_empresas')
    
    # Si la empresa actual es la que se va a desactivar, cambiar a otra empresa
    if str(empresa.id) == request.session.get('empresa_actual_id'):
        otra_empresa = Empresa.objects.filter(
            usuarios__usuario=request.user,
            activo=True
        ).exclude(id=empresa.id).first()
        
        if otra_empresa:
            request.session['empresa_actual_id'] = str(otra_empresa.id)
    
    # Desactivar la empresa
    empresa.activo = False
    empresa.save()
    
    messages.success(request, f'Empresa {empresa.nombre} desactivada correctamente')
    return redirect('empresa:listar_empresas')

@login_required
def crear_empresa_inicial(request):
    if request.method == 'POST':
        try:
            # Crear la empresa
            empresa = Empresa.objects.create(
                razon_social=request.POST.get('razon_social'),
                nombre_fantasia=request.POST.get('nombre_fantasia'),
                ruc=request.POST.get('ruc'),
                direccion=request.POST.get('direccion'),
                telefono=request.POST.get('telefono'),
                email=request.POST.get('email'),
                representante_legal=request.POST.get('representante_legal'),
                fecha_inicio_licencia=date.today(),
                fecha_fin_licencia=date.today() + timedelta(days=365),
                activo=True
            )
            
            # Asignar el usuario como administrador de la empresa
            UsuarioEmpresa.objects.create(
                usuario=request.user,
                empresa=empresa,
                es_administrador=True,
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
    empresa = get_object_or_404(Empresa, id=request.session.get('empresa_id'), activo=True)
    
    if not UsuarioEmpresa.objects.filter(
        usuario=request.user, 
        empresa=empresa, 
        es_administrador=True
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