from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

def actualizar_detalles(apps, schema_editor):
    DetalleTratamiento = apps.get_model('tratamientos', 'DetalleTratamiento')
    for detalle in DetalleTratamiento.objects.all():
        if not detalle.profesional and detalle.tratamiento:
            detalle.profesional = detalle.tratamiento.profesional
            detalle.save()

class Migration(migrations.Migration):
    dependencies = [
        ('tratamientos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalletratamiento',
            name='fecha_creacion',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AddField(
            model_name='detalletratamiento',
            name='fecha_actualizacion',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.RunPython(actualizar_detalles),
    ] 