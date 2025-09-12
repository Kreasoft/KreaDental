import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from profesionales.models import Especialidad, Profesional
from pacientes.models import Paciente
from procedimientos.models import Procedimiento
from empresa.models import Empresa
from prevision.models import Prevision

class Command(BaseCommand):
    help = 'Carga datos iniciales para la aplicación'

    def handle(self, *args, **kwargs):
        try:
            # Cargar datos iniciales
            with open('datos_iniciales.json', 'r', encoding='utf-8') as f:
                datos_iniciales = json.load(f)
            
            # Cargar datos adicionales
            with open('datos_iniciales_adicionales.json', 'r', encoding='utf-8') as f:
                datos_adicionales = json.load(f)
            
            # Combinar todos los datos
            todos_datos = datos_iniciales + datos_adicionales
            
            # Mapeo de modelos
            model_map = {
                'profesionales.especialidad': Especialidad,
                'profesionales.profesional': Profesional,
                'pacientes.paciente': Paciente,
                'procedimientos.procedimiento': Procedimiento
            }
            
            # Crear previsiones básicas si no existen
            previsiones = {
                'FONASA': Prevision.objects.get_or_create(nombre='FONASA')[0],
                'ISAPRE': Prevision.objects.get_or_create(nombre='ISAPRE')[0]
            }
            
            # Cargar datos en la base de datos
            with transaction.atomic():
                for dato in todos_datos:
                    model_name = dato['model']
                    fields = dato['fields']
                    
                    # Obtener la clase del modelo
                    ModelClass = model_map[model_name]
                    
                    # Si el modelo es Especialidad, buscar la instancia de Empresa
                    if model_name == 'profesionales.especialidad' and 'empresa' in fields:
                        empresa_id = fields.pop('empresa')
                        empresa = Empresa.objects.get(id=empresa_id)
                        fields['empresa'] = empresa
                    
                    # Si el modelo es Profesional, buscar la instancia de Especialidad y Empresa
                    if model_name == 'profesionales.profesional':
                        if 'especialidad' in fields:
                            especialidad_id = fields.pop('especialidad')
                            especialidad = Especialidad.objects.get(id=especialidad_id)
                            fields['especialidad'] = especialidad
                        if 'empresa' in fields:
                            empresa_id = fields.pop('empresa')
                            empresa = Empresa.objects.get(id=empresa_id)
                            fields['empresa'] = empresa
                    
                    # Si el modelo es Paciente, mapear campos y buscar instancias
                    if model_name == 'pacientes.paciente':
                        # Mapear campos antiguos a nuevos
                        if 'nombres' in fields:
                            fields['nombre'] = fields.pop('nombres')
                        if 'apellido_paterno' in fields and 'apellido_materno' in fields:
                            fields['apellidos'] = f"{fields.pop('apellido_paterno')} {fields.pop('apellido_materno')}"
                        if 'rut' in fields:
                            fields['documento'] = fields.pop('rut')
                        if 'estado' in fields:
                            fields['activo'] = fields.pop('estado')
                        
                        # Buscar instancias relacionadas
                        if 'prevision' in fields:
                            prevision_nombre = fields.pop('prevision')
                            fields['prevision'] = previsiones.get(prevision_nombre)
                        if 'empresa' in fields:
                            empresa_id = fields.pop('empresa')
                            empresa = Empresa.objects.get(id=empresa_id)
                            fields['empresa'] = empresa
                    
                    # Si el modelo es Procedimiento, eliminar el campo empresa si existe y asignar especialidad
                    if model_name == 'procedimientos.procedimiento':
                        if 'empresa' in fields:
                            fields.pop('empresa')
                        if 'especialidad' in fields:
                            especialidad_id = fields.pop('especialidad')
                            especialidad = Especialidad.objects.get(id=especialidad_id)
                            fields['especialidad'] = especialidad
                    
                    # Crear o actualizar el objeto
                    obj, created = ModelClass.objects.update_or_create(
                        id=dato['pk'],
                        defaults=fields
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Creado {model_name} {obj}')
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f'Actualizado {model_name} {obj}')
                        )
            
            self.stdout.write(
                self.style.SUCCESS('Datos cargados exitosamente')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al cargar datos: {str(e)}')
            ) 