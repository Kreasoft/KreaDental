from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('documento', models.CharField(max_length=20, unique=True)),
                ('especialidad', models.CharField(choices=[('medicina_general', 'Medicina General'), ('pediatria', 'Pediatría'), ('ginecologia', 'Ginecología'), ('cardiologia', 'Cardiología'), ('dermatologia', 'Dermatología'), ('oftalmologia', 'Oftalmología'), ('otorrinolaringologia', 'Otorrinolaringología'), ('psiquiatria', 'Psiquiatría'), ('traumatologia', 'Traumatología'), ('urologia', 'Urología')], max_length=50)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('comuna', models.CharField(default='Providencia', max_length=100)),
                ('ciudad', models.CharField(default='Santiago', max_length=100)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profesional', to='auth.user')),
            ],
            options={
                'verbose_name': 'Profesional',
                'verbose_name_plural': 'Profesionales',
                'ordering': ['apellidos', 'nombre'],
            },
        ),
    ] 