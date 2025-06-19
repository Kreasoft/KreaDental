from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Prevision
from .forms import PrevisionForm


def lista_previsiones(request):
    previsiones = Prevision.objects.all()
    return render(request, 'prevision/lista_previsiones_dental.html', {'previsiones': previsiones})

def crear_prevision(request):
    if request.method == 'POST':
        form = PrevisionForm(request.POST)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Previsión creada correctamente')
            return redirect('prevision:lista_previsiones')
    else:
        form = PrevisionForm()
    return render(request, 'prevision/crear_prevision_dental.html', {'form': form})            

def editar_prevision(request, prevision_id):
    prevision = get_object_or_404(Prevision, id=prevision_id)
    if request.method == 'POST':
        form = PrevisionForm(request.POST, instance=prevision)
        if form.is_valid():         
            form.save()
            messages.success(request, 'Previsión actualizada correctamente')
            return redirect('prevision:lista_previsiones')
    else:
        form = PrevisionForm(instance=prevision)
    return render(request, 'prevision/crear_prevision_dental.html', {'form': form})

def eliminar_prevision(request, prevision_id):
    prevision = get_object_or_404(Prevision, id=prevision_id)
    prevision.delete()
    messages.success(request, 'Previsión eliminada correctamente')
    return redirect('prevision:lista_previsiones')

    