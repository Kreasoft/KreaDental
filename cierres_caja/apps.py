from django.apps import AppConfig


class CierresCajaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cierres_caja'
    verbose_name = 'Cierres de Caja'

    def ready(self):
        try:
            import cierres_caja.signals
        except ImportError:
            pass
