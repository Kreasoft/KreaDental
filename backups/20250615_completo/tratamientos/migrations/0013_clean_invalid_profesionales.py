from django.db import migrations

def limpiar_profesionales_invalidos(apps, schema_editor):
    Tratamiento = apps.get_model('tratamientos', 'Tratamiento')
    DetalleTratamiento = apps.get_model('tratamientos', 'DetalleTratamiento')
    Profesional = apps.get_model('profesionales', 'Profesional')

    # Obtener IDs válidos de profesionales
    profesionales_ids = set(Profesional.objects.values_list('id', flat=True))

    # Limpiar tratamientos con profesionales inválidos
    Tratamiento.objects.exclude(profesional_id__in=profesionales_ids).update(profesional=None)
    DetalleTratamiento.objects.exclude(profesional_id__in=profesionales_ids).update(profesional=None)

class Migration(migrations.Migration):

    dependencies = [
        ('tratamientos', '0012_merge_20250501_2346'),
    ]

    operations = [
        migrations.RunPython(limpiar_profesionales_invalidos),
    ]
