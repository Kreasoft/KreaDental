from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Sum, FloatField
from django.db.models.functions import Cast
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from pacientes.models import Paciente
from citas.models import Cita
from tratamientos.models import Tratamiento
from profesionales.models import Profesional
from pagos_tratamientos.models import PagoTratamiento

@login_required
def dashboard(request):
    # Obtener fechas para filtrado
    fecha_fin = request.GET.get('fecha_fin', timezone.now().date())
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    fecha_inicio = request.GET.get('fecha_inicio', (fecha_fin - timedelta(days=30)))
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()

    # Estadísticas generales
    total_pacientes = Paciente.objects.count()
    total_citas = Cita.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).count()
    total_tratamientos = Tratamiento.objects.filter(fecha_inicio__range=[fecha_inicio, fecha_fin]).count()
    ingresos_totales = Tratamiento.objects.filter(
        fecha_inicio__range=[fecha_inicio, fecha_fin]
    ).aggregate(total=Sum('costo_total'))['total'] or 0

    # Gráficos para el dashboard
    citas_por_dia = Cita.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin]
    ).values('fecha').annotate(total=Count('id')).order_by('fecha')

    tratamientos_por_dia = Tratamiento.objects.filter(
        fecha_inicio__range=[fecha_inicio, fecha_fin]
    ).values('fecha_inicio').annotate(total=Count('id')).order_by('fecha_inicio')

    # Crear gráficos con Plotly
    fig_citas = go.Figure()
    fig_citas.add_trace(go.Scatter(
        x=[x['fecha'] for x in citas_por_dia],
        y=[x['total'] for x in citas_por_dia],
        name='Citas',
        mode='lines+markers'
    ))
    fig_citas.update_layout(
        title='Citas por Día',
        xaxis_title='Fecha',
        yaxis_title='Número de Citas'
    )

    fig_tratamientos = go.Figure()
    fig_tratamientos.add_trace(go.Scatter(
        x=[x['fecha_inicio'] for x in tratamientos_por_dia],
        y=[x['total'] for x in tratamientos_por_dia],
        name='Tratamientos',
        mode='lines+markers'
    ))
    fig_tratamientos.update_layout(
        title='Tratamientos por Día',
        xaxis_title='Fecha',
        yaxis_title='Número de Tratamientos'
    )

    context = {
        'total_pacientes': total_pacientes,
        'total_citas': total_citas,
        'total_tratamientos': total_tratamientos,
        'ingresos_totales': ingresos_totales,
        'grafico_citas': fig_citas.to_html(full_html=False),
        'grafico_tratamientos': fig_tratamientos.to_html(full_html=False),
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'informes/dashboard.html', context)

@login_required
def informe_tratamientos(request):
    fecha_fin = request.GET.get('fecha_fin', timezone.now().date())
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    fecha_inicio = request.GET.get('fecha_inicio', (fecha_fin - timedelta(days=30)))
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()

    profesional_id = request.GET.get('profesional')

    # Base queryset
    tratamientos = Tratamiento.objects.filter(fecha_inicio__range=[fecha_inicio, fecha_fin])
    pagos = PagoTratamiento.objects.filter(fecha_pago__range=[fecha_inicio, fecha_fin], estado='COMPLETADO')
    if profesional_id:
        tratamientos = tratamientos.filter(profesional_id=profesional_id)
        pagos = pagos.filter(tratamiento__profesional_id=profesional_id)

    # Análisis de tratamientos
    tratamientos_por_estado = tratamientos.values('estado').annotate(
        total=Count('id'),
        ingresos=Sum('costo_total')
    )

    tratamientos_por_profesional = tratamientos.values(
        'profesional__nombres', 
        'profesional__apellido_paterno'
    ).annotate(
        total=Count('id'),
        ingresos=Sum('costo_total')
    )

    # Análisis de ingresos por día (tratamientos)
    ingresos_por_dia = tratamientos.values('fecha_inicio').annotate(
        total=Sum('costo_total')
    ).order_by('fecha_inicio')

    # Análisis de pagos por día
    pagos_por_dia = pagos.values('fecha_pago').annotate(
        total=Sum('monto')
    ).order_by('fecha_pago')

    # Crear gráficos
    fig_estados = px.pie(
        pd.DataFrame(list(tratamientos_por_estado)),
        values='total',
        names='estado',
        title='Tratamientos por Estado'
    )

    fig_ingresos = go.Figure()
    fig_ingresos.add_trace(go.Scatter(
        x=[x['fecha_inicio'] for x in ingresos_por_dia],
        y=[x['total'] for x in ingresos_por_dia],
        name='Ingresos Totales',
        mode='lines+markers'
    ))
    fig_ingresos.add_trace(go.Scatter(
        x=[x['fecha_pago'] for x in pagos_por_dia],
        y=[x['total'] for x in pagos_por_dia],
        name='Pagos Recibidos',
        mode='lines+markers'
    ))
    fig_ingresos.update_layout(
        title='Ingresos y Pagos por Día',
        xaxis_title='Fecha',
        yaxis_title='Monto'
    )

    fig_ingresos_profesionales = px.bar(
        pd.DataFrame(list(tratamientos_por_profesional)),
        x='profesional__nombres',
        y='ingresos',
        title='Ingresos por Profesional',
        labels={'profesional__nombres': 'Profesional', 'ingresos': 'Ingresos'}
    )

    context = {
        'tratamientos': tratamientos,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'profesionales': Profesional.objects.filter(activo=True),
        'profesional_id': profesional_id,
        'grafico_estados': fig_estados.to_html(full_html=False),
        'grafico_ingresos': fig_ingresos.to_html(full_html=False),
        'grafico_ingresos_profesionales': fig_ingresos_profesionales.to_html(full_html=False),
        'total_tratamientos': tratamientos.count(),
        'total_ingresos': tratamientos.aggregate(total=Sum('costo_total'))['total'] or 0,
    }
    return render(request, 'informes/tratamientos.html', context)

@login_required
def informe_financiero(request):
    # Obtener fechas
    fecha_fin = request.GET.get('fecha_fin', timezone.now().date())
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    fecha_inicio = request.GET.get('fecha_inicio', (fecha_fin - timedelta(days=30)))
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        
    print(f'\nDEBUG - Fechas:')
    print(f'Fecha inicio: {fecha_inicio}')
    print(f'Fecha fin: {fecha_fin}')

    # 1. Obtener tratamientos del período
    tratamientos = Tratamiento.objects.filter(
        fecha_inicio__range=[fecha_inicio, fecha_fin]
    )
    
    # 2. Obtener pagos del período
    pagos = PagoTratamiento.objects.filter(
        fecha_pago__range=[fecha_inicio, fecha_fin],
        estado='COMPLETADO'
    )
    
    print('\nDEBUG - Consultas:')
    print(f'Número de tratamientos: {tratamientos.count()}')
    print(f'Número de pagos: {pagos.count()}')

    # Análisis de ingresos por día (tratamientos)
    ingresos_por_dia = tratamientos.values('fecha_inicio').annotate(
        total=Sum('costo_total')
    ).order_by('fecha_inicio')

    # Análisis de pagos por día
    pagos_por_dia = pagos.values('fecha_pago').annotate(
        total=Sum('monto')
    ).order_by('fecha_pago')

    # Análisis de ingresos por profesional
    ingresos_por_profesional = tratamientos.values(
        'profesional__nombres',
        'profesional__apellido_paterno'
    ).annotate(
        total=Sum('costo_total'),
        num_tratamientos=Count('id'),
        promedio=Cast(Sum('costo_total'), FloatField()) / Cast(Count('id'), FloatField())
    ).order_by('-total')

    # Crear gráficos
    fig_ingresos = go.Figure()
    fig_ingresos.add_trace(go.Scatter(
        x=[x['fecha_inicio'] for x in ingresos_por_dia],
        y=[x['total'] for x in ingresos_por_dia],
        name='Ingresos Totales',
        mode='lines+markers'
    ))
    fig_ingresos.add_trace(go.Scatter(
        x=[x['fecha_pago'] for x in pagos_por_dia],
        y=[x['total'] for x in pagos_por_dia],
        name='Pagos Recibidos',
        mode='lines+markers'
    ))
    fig_ingresos.update_layout(
        title='Ingresos y Pagos por Día',
        xaxis_title='Fecha',
        yaxis_title='Monto'
    )

    # Gráfico de barras para ingresos por profesional
    df_profesionales = pd.DataFrame(list(ingresos_por_profesional))
    if not df_profesionales.empty:
        df_profesionales['nombre_completo'] = df_profesionales['profesional__nombres'] + ' ' + df_profesionales['profesional__apellido_paterno']
        fig_prof = px.bar(
            df_profesionales,
            x='nombre_completo',
            y='total',
            title='Ingresos por Profesional',
            labels={'nombre_completo': 'Profesional', 'total': 'Ingresos'}
        )
    else:
        fig_prof = go.Figure()

    # 3. Calcular totales
    ingresos_totales = tratamientos.aggregate(
        total=Sum('costo_total')
    )['total'] or 0
    
    # Total pagado: todos los pagos completados de los tratamientos del período
    total_pagado = PagoTratamiento.objects.filter(
        tratamiento__in=tratamientos,
        estado='COMPLETADO'
    ).aggregate(
        total=Sum('monto')
    )['total'] or 0
    
    # Total pendiente: ingresos totales menos lo que ya se ha pagado
    total_pendiente = ingresos_totales - total_pagado
    
    print('\nDEBUG - Totales:')
    print(f'Ingresos totales: ${ingresos_totales:,.0f}')
    print(f'Total pagado: ${total_pagado:,.0f}')
    print(f'Total pendiente: ${total_pendiente:,.0f}')

    # 4. Preparar contexto
    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'grafico_ingresos': fig_ingresos.to_html(full_html=False),
        'grafico_profesionales': fig_prof.to_html(full_html=False),
        'ingresos_totales': ingresos_totales,
        'total_pagado': total_pagado,
        'total_pendiente': total_pendiente,
        'num_tratamientos': tratamientos.count(),
        'ingresos_por_profesional': ingresos_por_profesional,
    }
    
    print('\nDEBUG - Contexto enviado al template:')
    print(f'ingresos_totales: ${context["ingresos_totales"]:,.0f}')
    print(f'total_pagado: ${context["total_pagado"]:,.0f}')
    print(f'total_pendiente: ${context["total_pendiente"]:,.0f}')
    return render(request, 'informes/financiero.html', context)

@login_required
def informe_pacientes(request):
    fecha_fin = request.GET.get('fecha_fin', timezone.now().date())
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    fecha_inicio = request.GET.get('fecha_inicio', (fecha_fin - timedelta(days=30)))
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()

    # Análisis de pacientes
    pacientes = Paciente.objects.all()
    pacientes_nuevos = pacientes.filter(fecha_registro__range=[fecha_inicio, fecha_fin])
    
    citas_por_paciente = Cita.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin]
    ).values(
        'paciente__nombre',
        'paciente__apellidos'
    ).annotate(
        total_citas=Count('id')
    ).order_by('-total_citas')

    tratamientos_por_paciente = Tratamiento.objects.filter(
        fecha_inicio__range=[fecha_inicio, fecha_fin]
    ).values(
        'paciente__nombre',
        'paciente__apellidos'
    ).annotate(
        total_tratamientos=Count('id'),
        total_gastos=Sum('costo_total')
    ).order_by('-total_gastos')

    # Crear gráficos
    df_citas = pd.DataFrame(list(citas_por_paciente))
    if not df_citas.empty:
        df_citas['nombre_completo'] = df_citas['paciente__nombre'] + ' ' + df_citas['paciente__apellidos']
        fig_citas = px.bar(
            df_citas.head(10),  # Top 10 pacientes
            x='nombre_completo',
            y='total_citas',
            title='Top 10 Pacientes por Número de Citas',
            labels={'nombre_completo': 'Paciente', 'total_citas': 'Número de Citas'}
        )
    else:
        fig_citas = go.Figure()

    df_tratamientos = pd.DataFrame(list(tratamientos_por_paciente))
    if not df_tratamientos.empty:
        df_tratamientos['nombre_completo'] = df_tratamientos['paciente__nombre'] + ' ' + df_tratamientos['paciente__apellidos']
        fig_gastos = px.bar(
            df_tratamientos.head(10),  # Top 10 pacientes
            x='nombre_completo',
            y='total_gastos',
            title='Top 10 Pacientes por Gastos en Tratamientos',
            labels={'nombre_completo': 'Paciente', 'total_gastos': 'Total Gastos'}
        )
    else:
        fig_gastos = go.Figure()

    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_pacientes': pacientes.count(),
        'pacientes_nuevos': pacientes_nuevos.count(),
        'grafico_citas': fig_citas.to_html(full_html=False),
        'grafico_gastos': fig_gastos.to_html(full_html=False),
        'citas_por_paciente': citas_por_paciente[:10],  # Top 10
        'tratamientos_por_paciente': tratamientos_por_paciente[:10],  # Top 10
    }
    return render(request, 'informes/pacientes.html', context)
