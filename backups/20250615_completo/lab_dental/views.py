from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Laboratorio, TrabajoLaboratorio, SeguimientoTrabajo
from .forms import LaboratorioForm, TrabajoLaboratorioForm, SeguimientoTrabajoForm

@login_required
def lista_laboratorios(request):
    laboratorios = Laboratorio.objects.filter(activo=True)
    query = request.GET.get('q')
    if query:
        laboratorios = laboratorios.filter(
            Q(nombre__icontains=query) |
            Q(contacto__icontains=query) |
            Q(email__icontains=query)
        )
    
    paginator = Paginator(laboratorios, 10)
    page = request.GET.get('page')
    laboratorios = paginator.get_page(page)
    
    return render(request, 'lab_dental/lista_laboratorios.html', {
        'laboratorios': laboratorios,
        'query': query
    })

@login_required
def detalle_laboratorio(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    trabajos = laboratorio.trabajos.all().order_by('-fecha_creacion')[:5]
    
    return render(request, 'lab_dental/detalle_laboratorio.html', {
        'laboratorio': laboratorio,
        'trabajos_recientes': trabajos
    })

@login_required
def crear_laboratorio(request):
    if request.method == 'POST':
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            laboratorio = form.save(commit=False)
            laboratorio.creado_por = request.user
            laboratorio.save()
            messages.success(request, 'Laboratorio creado exitosamente.')
            return redirect('lab_dental:detalle_laboratorio', pk=laboratorio.pk)
    else:
        form = LaboratorioForm()
    
    return render(request, 'lab_dental/form_laboratorio.html', {
        'form': form,
        'titulo': 'Crear Laboratorio'
    })

@login_required
def editar_laboratorio(request, pk):
    laboratorio = get_object_or_404(Laboratorio, pk=pk)
    if request.method == 'POST':
        form = LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laboratorio actualizado exitosamente.')
            return redirect('lab_dental:detalle_laboratorio', pk=laboratorio.pk)
    else:
        form = LaboratorioForm(instance=laboratorio)
    
    return render(request, 'lab_dental/form_laboratorio.html', {
        'form': form,
        'titulo': 'Editar Laboratorio',
        'laboratorio': laboratorio
    })

@login_required
def lista_trabajos(request):
    trabajos = TrabajoLaboratorio.objects.all()
    query = request.GET.get('q')
    estado = request.GET.get('estado')
    
    if query:
        trabajos = trabajos.filter(
            Q(paciente__nombre__icontains=query) |
            Q(laboratorio__nombre__icontains=query) |
            Q(tipo_trabajo__icontains=query)
        )
    
    if estado:
        trabajos = trabajos.filter(estado=estado)
    
    paginator = Paginator(trabajos, 10)
    page = request.GET.get('page')
    trabajos = paginator.get_page(page)
    
    return render(request, 'lab_dental/lista_trabajos.html', {
        'trabajos': trabajos,
        'query': query,
        'estado_seleccionado': estado,
        'estados': TrabajoLaboratorio.ESTADO_CHOICES
    })

@login_required
def crear_trabajo(request):
    if request.method == 'POST':
        form = TrabajoLaboratorioForm(request.POST)
        if form.is_valid():
            trabajo = form.save(commit=False)
            trabajo.creado_por = request.user
            trabajo.save()
            
            # Crear el primer seguimiento
            SeguimientoTrabajo.objects.create(
                trabajo=trabajo,
                estado=trabajo.estado,
                notas='Trabajo creado',
                creado_por=request.user
            )
            
            messages.success(request, 'Trabajo de laboratorio creado exitosamente.')
            return redirect('lab_dental:detalle_trabajo', pk=trabajo.pk)
    else:
        form = TrabajoLaboratorioForm()
    
    return render(request, 'lab_dental/form_trabajo.html', {
        'form': form,
        'titulo': 'Crear Trabajo de Laboratorio'
    })

@login_required
def detalle_trabajo(request, pk):
    trabajo = get_object_or_404(TrabajoLaboratorio, pk=pk)
    seguimientos = trabajo.seguimientos.all().order_by('-fecha_creacion')
    
    if request.method == 'POST':
        form = SeguimientoTrabajoForm(request.POST)
        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.trabajo = trabajo
            seguimiento.creado_por = request.user
            seguimiento.save()
            
            # Actualizar el estado del trabajo
            trabajo.estado = seguimiento.estado
            trabajo.save()
            
            messages.success(request, 'Seguimiento agregado exitosamente.')
            return redirect('lab_dental:detalle_trabajo', pk=trabajo.pk)
    else:
        form = SeguimientoTrabajoForm()
    
    return render(request, 'lab_dental/detalle_trabajo.html', {
        'trabajo': trabajo,
        'seguimientos': seguimientos,
        'form': form
    })
