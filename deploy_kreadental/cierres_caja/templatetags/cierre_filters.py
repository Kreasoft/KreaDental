from django import template
from decimal import Decimal, InvalidOperation
import locale

register = template.Library()

@register.filter
def formatear_monto_sin_decimales(value):
    try:
        if value is None:
            return '0'
        num = Decimal(value)
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
        return locale.format_string("%.0f", num, grouping=True).replace('.', 'TEMP').replace(',', '.').replace('TEMP', '')
    except (InvalidOperation, ValueError, TypeError):
        return str(value) if value is not None else '0'
    finally:
        locale.setlocale(locale.LC_ALL, '')
