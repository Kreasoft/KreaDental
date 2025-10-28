from django.db import migrations

def limpiar_datos(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Tratamiento = apps.get_model('tratamientos', 'Tratamiento')
    DetalleTratamiento = apps.get_model('tratamientos', 'DetalleTratamiento')
    Profesional = apps.get_model('profesionales', 'Profesional')
    
    # Obtener IDs válidos de profesionales
    profesionales_validos = set(Profesional.objects.using(db_alias).values_list('id', flat=True))
    
    # Limpiar tratamientos
    Tratamiento.objects.using(db_alias).filter(profesional_id__isnull=False).exclude(
        profesional_id__in=profesionales_validos
    ).update(profesional_id=None)
    
    # Limpiar detalles de tratamientos
    DetalleTratamiento.objects.using(db_alias).filter(profesional_id__isnull=False).exclude(
        profesional_id__in=profesionales_validos
    ).update(profesional_id=None)

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('tratamientos', '0013_clean_invalid_profesionales'),
    ]

    operations = [
        migrations.RunPython(limpiar_datos, migrations.RunPython.noop),
    ]
