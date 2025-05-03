from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Empresa
from .forms import EmpresaForm

@login_required
def editar_empresa(request):
    # Obtener la primera empresa o crear una nueva si no existe
    empresa = Empresa.objects.first()
    if not empresa:
        empresa = Empresa()
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información de la empresa actualizada correctamente.')
            return redirect('empresa:editar_empresa')
    else:
        form = EmpresaForm(instance=empresa)
    
    return render(request, 'empresa/form_empresa.html', {
        'form': form,
        'empresa': empresa
    }) 