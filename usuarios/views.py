from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UsuarioUpdateForm

# Create your views here.

@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {
        'usuario': request.user
    })

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('usuarios:perfil')
    else:
        form = UsuarioUpdateForm(instance=request.user)
    
    return render(request, 'usuarios/editar_perfil.html', {
        'form': form
    })

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
            return redirect('usuarios:perfil')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'usuarios/cambiar_password.html', {
        'form': form
    })
