from django.apps import AppConfig

class TratamientosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tratamientos'
    verbose_name = 'Tratamientos'
    
    def ready(self):
        import tratamientos.signals 