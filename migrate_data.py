#!/usr/bin/env python
"""
Script para migrar datos de SQLite a PostgreSQL
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def configurar_sqlite():
    """Configurar Django para usar SQLite temporalmente"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Configuración temporal para SQLite
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
    
    django.setup()

def configurar_postgresql():
    """Configurar Django para usar PostgreSQL"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def exportar_datos_sqlite():
    """Exportar datos desde SQLite"""
    print("📤 Exportando datos desde SQLite...")
    
    try:
        # Exportar datos excluyendo tablas del sistema
        execute_from_command_line([
            'manage.py', 'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '-e', 'contenttypes',
            '-e', 'auth.Permission',
            '-e', 'sessions',
            '--output', 'datos_exportados.json'
        ])
        print("✅ Datos exportados exitosamente a 'datos_exportados.json'")
        return True
    except Exception as e:
        print(f"❌ Error al exportar datos: {e}")
        return False

def importar_datos_postgresql():
    """Importar datos a PostgreSQL"""
    print("📥 Importando datos a PostgreSQL...")
    
    try:
        execute_from_command_line([
            'manage.py', 'loaddata', 'datos_exportados.json'
        ])
        print("✅ Datos importados exitosamente a PostgreSQL")
        return True
    except Exception as e:
        print(f"❌ Error al importar datos: {e}")
        return False

def verificar_datos():
    """Verificar que los datos se migraron correctamente"""
    print("🔍 Verificando migración de datos...")
    
    try:
        from django.contrib.auth.models import User
        from pacientes.models import Paciente
        from profesionales.models import Profesional
        from citas.models import Cita
        
        # Verificar usuarios
        user_count = User.objects.count()
        print(f"   👥 Usuarios: {user_count}")
        
        # Verificar pacientes
        paciente_count = Paciente.objects.count()
        print(f"   🏥 Pacientes: {paciente_count}")
        
        # Verificar profesionales
        profesional_count = Profesional.objects.count()
        print(f"   👨‍⚕️ Profesionales: {profesional_count}")
        
        # Verificar citas
        cita_count = Cita.objects.count()
        print(f"   📅 Citas: {cita_count}")
        
        print("✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en la verificación: {e}")
        return False

def main():
    """Función principal de migración"""
    print("🚀 Iniciando migración de datos SQLite → PostgreSQL")
    print("=" * 60)
    
    # Verificar que existe el archivo de datos
    if not os.path.exists('db.sqlite3'):
        print("❌ No se encontró el archivo db.sqlite3")
        return False
    
    # Verificar que existe el archivo de datos exportados
    if not os.path.exists('datos_exportados.json'):
        print("❌ No se encontró el archivo datos_exportados.json")
        print("   Ejecuta primero: python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json")
        return False
    
    # Configurar PostgreSQL
    configurar_postgresql()
    
    # Importar datos
    if importar_datos_postgresql():
        # Verificar datos
        if verificar_datos():
            print("\n🎉 Migración completada exitosamente!")
            print("   Los datos han sido migrados de SQLite a PostgreSQL")
            return True
    
    print("\n❌ La migración falló")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


"""
Script para migrar datos de SQLite a PostgreSQL
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def configurar_sqlite():
    """Configurar Django para usar SQLite temporalmente"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Configuración temporal para SQLite
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
    
    django.setup()

def configurar_postgresql():
    """Configurar Django para usar PostgreSQL"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def exportar_datos_sqlite():
    """Exportar datos desde SQLite"""
    print("📤 Exportando datos desde SQLite...")
    
    try:
        # Exportar datos excluyendo tablas del sistema
        execute_from_command_line([
            'manage.py', 'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '-e', 'contenttypes',
            '-e', 'auth.Permission',
            '-e', 'sessions',
            '--output', 'datos_exportados.json'
        ])
        print("✅ Datos exportados exitosamente a 'datos_exportados.json'")
        return True
    except Exception as e:
        print(f"❌ Error al exportar datos: {e}")
        return False

def importar_datos_postgresql():
    """Importar datos a PostgreSQL"""
    print("📥 Importando datos a PostgreSQL...")
    
    try:
        execute_from_command_line([
            'manage.py', 'loaddata', 'datos_exportados.json'
        ])
        print("✅ Datos importados exitosamente a PostgreSQL")
        return True
    except Exception as e:
        print(f"❌ Error al importar datos: {e}")
        return False

def verificar_datos():
    """Verificar que los datos se migraron correctamente"""
    print("🔍 Verificando migración de datos...")
    
    try:
        from django.contrib.auth.models import User
        from pacientes.models import Paciente
        from profesionales.models import Profesional
        from citas.models import Cita
        
        # Verificar usuarios
        user_count = User.objects.count()
        print(f"   👥 Usuarios: {user_count}")
        
        # Verificar pacientes
        paciente_count = Paciente.objects.count()
        print(f"   🏥 Pacientes: {paciente_count}")
        
        # Verificar profesionales
        profesional_count = Profesional.objects.count()
        print(f"   👨‍⚕️ Profesionales: {profesional_count}")
        
        # Verificar citas
        cita_count = Cita.objects.count()
        print(f"   📅 Citas: {cita_count}")
        
        print("✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en la verificación: {e}")
        return False

def main():
    """Función principal de migración"""
    print("🚀 Iniciando migración de datos SQLite → PostgreSQL")
    print("=" * 60)
    
    # Verificar que existe el archivo de datos
    if not os.path.exists('db.sqlite3'):
        print("❌ No se encontró el archivo db.sqlite3")
        return False
    
    # Verificar que existe el archivo de datos exportados
    if not os.path.exists('datos_exportados.json'):
        print("❌ No se encontró el archivo datos_exportados.json")
        print("   Ejecuta primero: python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json")
        return False
    
    # Configurar PostgreSQL
    configurar_postgresql()
    
    # Importar datos
    if importar_datos_postgresql():
        # Verificar datos
        if verificar_datos():
            print("\n🎉 Migración completada exitosamente!")
            print("   Los datos han sido migrados de SQLite a PostgreSQL")
            return True
    
    print("\n❌ La migración falló")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)





