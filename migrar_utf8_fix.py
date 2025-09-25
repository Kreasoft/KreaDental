#!/usr/bin/env python
"""
Script para migrar con configuración UTF-8 limpia
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

def crear_configuracion_limpia():
    """Crea una configuración de PostgreSQL completamente limpia"""
    print("\n🔧 Creando configuración limpia...")
    
    settings_file = "config/settings.py"
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar configuración de base de datos con configuración limpia
        old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kreadental_final',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}"""
        
        new_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kreadental_final',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}"""
        
        content = content.replace(old_config, new_config)
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuración limpia creada")
        return True
    except Exception as e:
        print(f"❌ Error creando configuración: {e}")
        return False

def crear_base_datos_limpia():
    """Crea una base de datos PostgreSQL con configuración limpia"""
    print("\n🗄️ Creando base de datos limpia...")
    
    # Eliminar base de datos existente
    ejecutar_comando('psql -U postgres -c "DROP DATABASE IF EXISTS kreadental_final;"', "Eliminando base de datos existente")
    
    # Crear nueva base de datos con configuración limpia
    if not ejecutar_comando('psql -U postgres -c "CREATE DATABASE kreadental_final WITH ENCODING \'UTF8\' LC_COLLATE=\'C\' LC_CTYPE=\'C\' TEMPLATE=template0;"', "Creando base de datos limpia"):
        return False
    
    return True

def aplicar_migraciones_limpias():
    """Aplica migraciones con configuración limpia"""
    print("\n🔄 Aplicando migraciones limpias...")
    
    # Verificar conexión
    if not ejecutar_comando("python manage.py check", "Verificando conexión limpia"):
        return False
    
    # Aplicar migraciones
    if not ejecutar_comando("python manage.py migrate", "Aplicando migraciones limpias"):
        return False
    
    return True

def importar_datos_limpos():
    """Importa datos con configuración limpia"""
    print("\n📥 Importando datos limpios...")
    
    if not ejecutar_comando("python manage.py loaddata datos_exportados.json", "Importando datos limpios"):
        return False
    
    return True

def verificar_migracion_limpia():
    """Verifica que la migración limpia fue exitosa"""
    print("\n🔍 Verificando migración limpia...")
    
    # Verificar que Django funciona
    if not ejecutar_comando("python manage.py check", "Verificando configuración Django limpia"):
        return False
    
    # Verificar tablas en PostgreSQL
    if not ejecutar_comando('psql -U postgres -d kreadental_final -c "\\dt"', "Verificando tablas en PostgreSQL limpio"):
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando migración con configuración UTF-8 limpia...")
    
    # Paso 1: Crear configuración limpia
    if not crear_configuracion_limpia():
        print("❌ No se pudo crear la configuración limpia")
        return
    
    # Paso 2: Crear base de datos limpia
    if not crear_base_datos_limpia():
        print("❌ No se pudo crear la base de datos limpia")
        return
    
    # Paso 3: Aplicar migraciones limpias
    if not aplicar_migraciones_limpias():
        print("❌ No se pudieron aplicar las migraciones limpias")
        return
    
    # Paso 4: Importar datos limpios
    if not importar_datos_limpos():
        print("❌ No se pudieron importar los datos limpios")
        return
    
    # Paso 5: Verificar migración limpia
    if not verificar_migracion_limpia():
        print("❌ La migración limpia no se completó correctamente")
        return
    
    print("\n🎉 ¡Migración con configuración limpia completada exitosamente!")
    print("📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Verifica que la aplicación funciona en el navegador")

if __name__ == "__main__":
    main()

"""
Script para migrar con configuración UTF-8 limpia
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

def crear_configuracion_limpia():
    """Crea una configuración de PostgreSQL completamente limpia"""
    print("\n🔧 Creando configuración limpia...")
    
    settings_file = "config/settings.py"
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar configuración de base de datos con configuración limpia
        old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kreadental_final',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}"""
        
        new_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kreadental_final',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}"""
        
        content = content.replace(old_config, new_config)
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuración limpia creada")
        return True
    except Exception as e:
        print(f"❌ Error creando configuración: {e}")
        return False

def crear_base_datos_limpia():
    """Crea una base de datos PostgreSQL con configuración limpia"""
    print("\n🗄️ Creando base de datos limpia...")
    
    # Eliminar base de datos existente
    ejecutar_comando('psql -U postgres -c "DROP DATABASE IF EXISTS kreadental_final;"', "Eliminando base de datos existente")
    
    # Crear nueva base de datos con configuración limpia
    if not ejecutar_comando('psql -U postgres -c "CREATE DATABASE kreadental_final WITH ENCODING \'UTF8\' LC_COLLATE=\'C\' LC_CTYPE=\'C\' TEMPLATE=template0;"', "Creando base de datos limpia"):
        return False
    
    return True

def aplicar_migraciones_limpias():
    """Aplica migraciones con configuración limpia"""
    print("\n🔄 Aplicando migraciones limpias...")
    
    # Verificar conexión
    if not ejecutar_comando("python manage.py check", "Verificando conexión limpia"):
        return False
    
    # Aplicar migraciones
    if not ejecutar_comando("python manage.py migrate", "Aplicando migraciones limpias"):
        return False
    
    return True

def importar_datos_limpos():
    """Importa datos con configuración limpia"""
    print("\n📥 Importando datos limpios...")
    
    if not ejecutar_comando("python manage.py loaddata datos_exportados.json", "Importando datos limpios"):
        return False
    
    return True

def verificar_migracion_limpia():
    """Verifica que la migración limpia fue exitosa"""
    print("\n🔍 Verificando migración limpia...")
    
    # Verificar que Django funciona
    if not ejecutar_comando("python manage.py check", "Verificando configuración Django limpia"):
        return False
    
    # Verificar tablas en PostgreSQL
    if not ejecutar_comando('psql -U postgres -d kreadental_final -c "\\dt"', "Verificando tablas en PostgreSQL limpio"):
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando migración con configuración UTF-8 limpia...")
    
    # Paso 1: Crear configuración limpia
    if not crear_configuracion_limpia():
        print("❌ No se pudo crear la configuración limpia")
        return
    
    # Paso 2: Crear base de datos limpia
    if not crear_base_datos_limpia():
        print("❌ No se pudo crear la base de datos limpia")
        return
    
    # Paso 3: Aplicar migraciones limpias
    if not aplicar_migraciones_limpias():
        print("❌ No se pudieron aplicar las migraciones limpias")
        return
    
    # Paso 4: Importar datos limpios
    if not importar_datos_limpos():
        print("❌ No se pudieron importar los datos limpios")
        return
    
    # Paso 5: Verificar migración limpia
    if not verificar_migracion_limpia():
        print("❌ La migración limpia no se completó correctamente")
        return
    
    print("\n🎉 ¡Migración con configuración limpia completada exitosamente!")
    print("📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Verifica que la aplicación funciona en el navegador")

if __name__ == "__main__":
    main()










