from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def add_minutes(time_str, minutes):
    """
    Añade minutos a una hora dada
    """
    try:
        time = datetime.strptime(str(time_str), '%H:%M:%S')
        time = time + timedelta(minutes=int(minutes))
        return time.strftime('%H:%M:%S')
    except:
        return time_str

@register.filter
def get_estado_color(estado):
    """
    Retorna el color correspondiente al estado de la cita
    """
    colores = {
        'PENDIENTE': '#FFD700',    # Dorado suave (mismo que en calendario)
        'CONFIRMADA': '#90EE90',   # Verde claro (mismo que en calendario)
        'COMPLETADA': '#87CEEB',   # Azul claro (mismo que en calendario)
        'CANCELADA': '#FFB6C1'     # Rosa claro (mismo que en calendario)
    }
    return colores.get(estado, '#6c757d') 