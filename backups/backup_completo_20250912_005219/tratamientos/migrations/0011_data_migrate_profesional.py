from django.db import migrations

def migrate_profesional_data(apps, schema_editor):
    Tratamiento = apps.get_model('tratamientos', 'Tratamiento')
    DetalleTratamiento = apps.get_model('tratamientos', 'DetalleTratamiento')
    User = apps.get_model('auth', 'User')
    Profesional = apps.get_model('profesionales', 'Profesional')

    # Migrar tratamientos
    for tratamiento in Tratamiento.objects.all():
        if tratamiento.profesional_id:
            try:
                profesional = Profesional.objects.get(usuario_id=tratamiento.profesional_id)
                tratamiento.profesional = profesional
                tratamiento.save()
            except Profesional.DoesNotExist:
                tratamiento.profesional = None
                tratamiento.save()

    # Migrar detalles de tratamiento
    for detalle in DetalleTratamiento.objects.all():
        if detalle.profesional_id:
            try:
                profesional = Profesional.objects.get(usuario_id=detalle.profesional_id)
                detalle.profesional = profesional
                detalle.save()
            except Profesional.DoesNotExist:
                detalle.profesional = None
                detalle.save()

class Migration(migrations.Migration):
    dependencies = [
        ('tratamientos', '0010_alter_detalletratamiento_profesional_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_profesional_data),
    ]
