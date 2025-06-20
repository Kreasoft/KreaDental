from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import FormaPago
from .forms import FormaPagoForm

def lista_formas_pago(request):
    formas_pago = FormaPago.objects.all()
    return render(request, 'formas_pago/lista_formas_pago.html', {'formas_pago': formas_pago})

def crear_forma_pago(request):
    if request.method == 'POST':
        form = FormaPagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Forma de pago creada exitosamente.')
            return redirect('formas_pago:lista_formas_pago')
    else:
        form = FormaPagoForm()
    return render(request, 'formas_pago/crear_forma_pago.html', {'form': form})

def editar_forma_pago(request, pk):
    forma_pago = get_object_or_404(FormaPago, pk=pk)
    if request.method == 'POST':
        form = FormaPagoForm(request.POST, instance=forma_pago)
        if form.is_valid():
            form.save()
            messages.success(request, 'Forma de pago actualizada exitosamente.')
            return redirect('formas_pago:lista_formas_pago')
    else:
        form = FormaPagoForm(instance=forma_pago)
    return render(request, 'formas_pago/editar_forma_pago.html', {'form': form, 'forma_pago': forma_pago})

def eliminar_forma_pago(request, pk):
    forma_pago = get_object_or_404(FormaPago, pk=pk)
    forma_pago.delete()
    messages.success(request, 'Forma de pago eliminada exitosamente.')
    return redirect('formas_pago:lista_formas_pago')

def cambiar_estado_forma_pago(request, pk):
    if request.method == 'POST':
        forma_pago = get_object_or_404(FormaPago, pk=pk)
        forma_pago.estado = not forma_pago.estado
        forma_pago.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
