from django.apps import AppConfig

class EmpresasConfig(AppConfig):  # Cambiado a EmpresasConfig para coincidir con lo que busca
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empresa'
    verbose_name = 'Empresa' 