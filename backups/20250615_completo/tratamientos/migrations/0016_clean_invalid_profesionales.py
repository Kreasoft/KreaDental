from django.db import migrations

def clean_invalid_profesionales(apps, schema_editor):
    Tratamiento = apps.get_model('tratamientos', 'Tratamiento')
    DetalleTratamiento = apps.get_model('tratamientos', 'DetalleTratamiento')
    Profesional = apps.get_model('profesionales', 'Profesional')
    
    # Obtener IDs válidos de profesionales
    profesionales_ids = set(Profesional.objects.values_list('id', flat=True))
    
    # Limpiar tratamientos con profesionales inválidos
    Tratamiento.objects.filter(profesional_id__isnull=False).exclude(profesional_id__in=profesionales_ids).update(profesional=None)
    
    # Limpiar detalles de tratamientos con profesionales inválidos
    DetalleTratamiento.objects.filter(profesional_id__isnull=False).exclude(profesional_id__in=profesionales_ids).update(profesional=None)

class Migration(migrations.Migration):

    dependencies = [
        ('tratamientos', '0015_alter_detalletratamiento_profesional'),
        ('profesionales', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(clean_invalid_profesionales),
    ]
