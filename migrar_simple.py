#!/usr/bin/env python
"""
Script simple para migrar a PostgreSQL sin problemas de codificación
"""
import os
import sys
import subprocess
import json
from pathlib import Path

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {descripcion}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8')
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - Éxito")
            if resultado.stdout and len(resultado.stdout.strip()) > 0:
                print(f"Salida: {resultado.stdout.strip()}")
        else:
            print(f"❌ {descripcion} - Error")
            if resultado.stderr and len(resultado.stderr.strip()) > 0:
                print(f"Error: {resultado.stderr.strip()}")
        return resultado.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def crear_base_datos_simple():
    """Crea una base de datos PostgreSQL simple"""
    print("\n🗄️ Creando base de datos PostgreSQL simple...")
    
    # Eliminar base de datos existente
    ejecutar_comando('psql -U postgres -c "DROP DATABASE IF EXISTS kreadental_cloud;"', "Eliminando base de datos existente")
    
    # Crear nueva base de datos con configuración simple
    if not ejecutar_comando('psql -U postgres -c "CREATE DATABASE kreadental_cloud;"', "Creando base de datos simple"):
        return False
    
    return True

def cambiar_configuracion_postgresql():
    """Cambia la configuración a PostgreSQL con configuración simple"""
    print("\n🔄 Cambiando configuración a PostgreSQL...")
    
    settings_file = "config/settings.py"
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar configuración de base de datos
        old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
        
        new_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kreadental_cloud',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}"""
        
        content = content.replace(old_config, new_config)
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuración cambiada a PostgreSQL")
        return True
    except Exception as e:
        print(f"❌ Error cambiando configuración: {e}")
        return False

def exportar_datos_sqlite():
    """Exporta datos de SQLite"""
    print("\n📤 Exportando datos de SQLite...")
    
    # Verificar que estamos en SQLite
    if not ejecutar_comando("python manage.py check", "Verificando configuración SQLite"):
        return False
    
    # Exportar datos
    if not ejecutar_comando("python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json", "Exportando datos"):
        return False
    
    print("✅ Datos exportados correctamente")
    return True

def aplicar_migraciones_postgresql():
    """Aplica migraciones a PostgreSQL"""
    print("\n🔄 Aplicando migraciones a PostgreSQL...")
    
    # Verificar conexión
    if not ejecutar_comando("python manage.py check", "Verificando conexión PostgreSQL"):
        return False
    
    # Aplicar migraciones
    if not ejecutar_comando("python manage.py migrate", "Aplicando migraciones"):
        return False
    
    return True

def importar_datos_postgresql():
    """Importa datos a PostgreSQL"""
    print("\n📥 Importando datos a PostgreSQL...")
    
    if not ejecutar_comando("python manage.py loaddata datos_exportados.json", "Importando datos"):
        return False
    
    return True

def verificar_migracion():
    """Verifica que la migración fue exitosa"""
    print("\n🔍 Verificando migración...")
    
    # Verificar que Django funciona
    if not ejecutar_comando("python manage.py check", "Verificando configuración Django"):
        return False
    
    # Verificar tablas en PostgreSQL
    if not ejecutar_comando('psql -U postgres -d kreadental_cloud -c "\\dt"', "Verificando tablas en PostgreSQL"):
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando migración simple de SQLite a PostgreSQL...")
    
    # Paso 1: Exportar datos de SQLite
    if not exportar_datos_sqlite():
        print("❌ No se pudieron exportar los datos de SQLite")
        return
    
    # Paso 2: Crear base de datos PostgreSQL
    if not crear_base_datos_simple():
        print("❌ No se pudo crear la base de datos PostgreSQL")
        return
    
    # Paso 3: Cambiar a PostgreSQL
    if not cambiar_configuracion_postgresql():
        print("❌ No se pudo cambiar a PostgreSQL")
        return
    
    # Paso 4: Aplicar migraciones
    if not aplicar_migraciones_postgresql():
        print("❌ No se pudieron aplicar las migraciones")
        return
    
    # Paso 5: Importar datos
    if not importar_datos_postgresql():
        print("❌ No se pudieron importar los datos")
        return
    
    # Paso 6: Verificar migración
    if not verificar_migracion():
        print("❌ La migración no se completó correctamente")
        return
    
    print("\n🎉 ¡Migración completada exitosamente!")
    print("📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Verifica que la aplicación funciona en el navegador")

if __name__ == "__main__":
    main()

"""
Script simple para migrar a PostgreSQL sin problemas de codificación
"""
import os
import sys
import subprocess
import json
from pathlib import Path

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {descripcion}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8')
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - Éxito")
            if resultado.stdout and len(resultado.stdout.strip()) > 0:
                print(f"Salida: {resultado.stdout.strip()}")
        else:
            print(f"❌ {descripcion} - Error")
            if resultado.stderr and len(resultado.stderr.strip()) > 0:
                print(f"Error: {resultado.stderr.strip()}")
        return resultado.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def crear_base_datos_simple():
    """Crea una base de datos PostgreSQL simple"""
    print("\n🗄️ Creando base de datos PostgreSQL simple...")
    
    # Eliminar base de datos existente
    ejecutar_comando('psql -U postgres -c "DROP DATABASE IF EXISTS kreadental_cloud;"', "Eliminando base de datos existente")
    
    # Crear nueva base de datos con configuración simple
    if not ejecutar_comando('psql -U postgres -c "CREATE DATABASE kreadental_cloud;"', "Creando base de datos simple"):
        return False
    
    return True

def cambiar_configuracion_postgresql():
    """Cambia la configuración a PostgreSQL con configuración simple"""
    print("\n🔄 Cambiando configuración a PostgreSQL...")
    
    settings_file = "config/settings.py"
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar configuración de base de datos
        old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
        
        new_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kreadental_cloud',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}"""
        
        content = content.replace(old_config, new_config)
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuración cambiada a PostgreSQL")
        return True
    except Exception as e:
        print(f"❌ Error cambiando configuración: {e}")
        return False

def exportar_datos_sqlite():
    """Exporta datos de SQLite"""
    print("\n📤 Exportando datos de SQLite...")
    
    # Verificar que estamos en SQLite
    if not ejecutar_comando("python manage.py check", "Verificando configuración SQLite"):
        return False
    
    # Exportar datos
    if not ejecutar_comando("python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json", "Exportando datos"):
        return False
    
    print("✅ Datos exportados correctamente")
    return True

def aplicar_migraciones_postgresql():
    """Aplica migraciones a PostgreSQL"""
    print("\n🔄 Aplicando migraciones a PostgreSQL...")
    
    # Verificar conexión
    if not ejecutar_comando("python manage.py check", "Verificando conexión PostgreSQL"):
        return False
    
    # Aplicar migraciones
    if not ejecutar_comando("python manage.py migrate", "Aplicando migraciones"):
        return False
    
    return True

def importar_datos_postgresql():
    """Importa datos a PostgreSQL"""
    print("\n📥 Importando datos a PostgreSQL...")
    
    if not ejecutar_comando("python manage.py loaddata datos_exportados.json", "Importando datos"):
        return False
    
    return True

def verificar_migracion():
    """Verifica que la migración fue exitosa"""
    print("\n🔍 Verificando migración...")
    
    # Verificar que Django funciona
    if not ejecutar_comando("python manage.py check", "Verificando configuración Django"):
        return False
    
    # Verificar tablas en PostgreSQL
    if not ejecutar_comando('psql -U postgres -d kreadental_cloud -c "\\dt"', "Verificando tablas en PostgreSQL"):
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando migración simple de SQLite a PostgreSQL...")
    
    # Paso 1: Exportar datos de SQLite
    if not exportar_datos_sqlite():
        print("❌ No se pudieron exportar los datos de SQLite")
        return
    
    # Paso 2: Crear base de datos PostgreSQL
    if not crear_base_datos_simple():
        print("❌ No se pudo crear la base de datos PostgreSQL")
        return
    
    # Paso 3: Cambiar a PostgreSQL
    if not cambiar_configuracion_postgresql():
        print("❌ No se pudo cambiar a PostgreSQL")
        return
    
    # Paso 4: Aplicar migraciones
    if not aplicar_migraciones_postgresql():
        print("❌ No se pudieron aplicar las migraciones")
        return
    
    # Paso 5: Importar datos
    if not importar_datos_postgresql():
        print("❌ No se pudieron importar los datos")
        return
    
    # Paso 6: Verificar migración
    if not verificar_migracion():
        print("❌ La migración no se completó correctamente")
        return
    
    print("\n🎉 ¡Migración completada exitosamente!")
    print("📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Verifica que la aplicación funciona en el navegador")

if __name__ == "__main__":
    main()










