from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('tratamientos', '0002_actualizar_modelos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tratamiento',
            name='estado',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('EN_PROGRESO', 'En Progreso'), ('COMPLETADO', 'Completado'), ('CANCELADO', 'Cancelado')], default='PENDIENTE', max_length=20),
        ),
    ] 