from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ConfiguracionEmpresa
from .forms import ConfiguracionEmpresaForm

def es_administrador(user):
    return user.is_superuser

@login_required
@user_passes_test(es_administrador)
def configuracion_empresa(request):
    # Obtener la configuración existente o crear una nueva
    config = ConfiguracionEmpresa.objects.first()
    if not config:
        config = ConfiguracionEmpresa()

    if request.method == 'POST':
        form = ConfiguracionEmpresaForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración guardada exitosamente.')
            return redirect('configuracion:empresa')
    else:
        form = ConfiguracionEmpresaForm(instance=config)

    return render(request, 'configuracion/configuracion_empresa.html', {
        'form': form,
        'config': config
    })
