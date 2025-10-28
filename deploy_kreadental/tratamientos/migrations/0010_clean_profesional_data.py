from django.db import migrations

def clean_profesional_data(apps, schema_editor):
    # Primero limpiar los datos existentes
    Tratamiento = apps.get_model('tratamientos', 'Tratamiento')
    DetalleTratamiento = apps.get_model('tratamientos', 'DetalleTratamiento')
    
    # Establecer todos los profesionales a NULL
    Tratamiento.objects.all().update(profesional=None)
    DetalleTratamiento.objects.all().update(profesional=None)

class Migration(migrations.Migration):
    dependencies = [
        ('tratamientos', '0009_alter_detalletratamiento_profesional'),
    ]

    operations = [
        migrations.RunPython(clean_profesional_data),
    ]
