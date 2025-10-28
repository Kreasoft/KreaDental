from django import template
from decimal import Decimal, InvalidOperation
import locale

register = template.Library()

@register.filter
def formatear_monto_chileno(value):
    try:
        num = Decimal(value)
        # Configurar locale para formato chileno (punto miles, coma decimal)
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
        return locale.format_string("%.2f", num, grouping=True).replace('.', 'TEMP').replace(',', '.').replace('TEMP', ',')
    except (InvalidOperation, ValueError):
        return value
    finally:
        locale.setlocale(locale.LC_ALL, '') # Restaurar locale por defecto

@register.filter
def formatear_monto_sin_decimales(value):
    try:
        num = Decimal(value)
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
        return locale.format_string("%.0f", num, grouping=True).replace('.', 'TEMP').replace(',', '.').replace('TEMP', '')
    except (InvalidOperation, ValueError):
        return value
    finally:
        locale.setlocale(locale.LC_ALL, '')

@register.filter
def formatear_monto_input(value):
    try:
        num = Decimal(value)
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
        return locale.format_string("%.2f", num, grouping=False).replace('.', ',') # Para input, sin separador de miles, coma decimal
    except (InvalidOperation, ValueError):
        return value
    finally:
        locale.setlocale(locale.LC_ALL, '')