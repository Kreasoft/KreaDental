#!/usr/bin/env python
"""
Script final para migración a PostgreSQL en producción
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

def configurar_postgresql_para_produccion():
    """Configura PostgreSQL para producción"""
    print("\n🔧 Configurando PostgreSQL para producción...")
    
    # Crear base de datos
    if not ejecutar_comando('psql -U postgres -c "CREATE DATABASE kreadental_cloud;"', "Creando base de datos kreadental_cloud"):
        print("⚠️ La base de datos ya existe o hay un error de permisos")
    
    return True

def cambiar_a_postgresql():
    """Cambia la configuración a PostgreSQL"""
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

def verificar_migracion_completa():
    """Verifica que la migración completa fue exitosa"""
    print("\n🔍 Verificando migración completa...")
    
    # Verificar que Django funciona
    if not ejecutar_comando("python manage.py check", "Verificando configuración Django"):
        return False
    
    # Verificar tablas en PostgreSQL
    if not ejecutar_comando('psql -U postgres -d kreadental_cloud -c "\\dt"', "Verificando tablas en PostgreSQL"):
        return False
    
    return True

def iniciar_servidor():
    """Inicia el servidor Django"""
    print("\n🚀 Iniciando servidor Django...")
    
    print("✅ Servidor iniciado. Accede a: http://127.0.0.1:8000")
    print("📋 Para detener el servidor presiona Ctrl+C")
    
    # Iniciar servidor en background
    subprocess.Popen(['python', 'manage.py', 'runserver'], shell=True)
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando migración final a PostgreSQL para producción...")
    
    # Paso 1: Exportar datos de SQLite
    if not exportar_datos_sqlite():
        print("❌ No se pudieron exportar los datos de SQLite")
        return
    
    # Paso 2: Configurar PostgreSQL
    if not configurar_postgresql_para_produccion():
        print("❌ No se pudo configurar PostgreSQL")
        return
    
    # Paso 3: Cambiar a PostgreSQL
    if not cambiar_a_postgresql():
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
    
    # Paso 6: Verificar migración completa
    if not verificar_migracion_completa():
        print("❌ La migración no se completó correctamente")
        return
    
    # Paso 7: Iniciar servidor
    if not iniciar_servidor():
        print("❌ No se pudo iniciar el servidor")
        return
    
    print("\n🎉 ¡Migración a PostgreSQL completada exitosamente!")
    print("📋 Tu aplicación está lista para producción con PostgreSQL")
    print("🔗 Accede a: http://127.0.0.1:8000")

if __name__ == "__main__":
    main()

"""
Script final para migración a PostgreSQL en producción
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

def configurar_postgresql_para_produccion():
    """Configura PostgreSQL para producción"""
    print("\n🔧 Configurando PostgreSQL para producción...")
    
    # Crear base de datos
    if not ejecutar_comando('psql -U postgres -c "CREATE DATABASE kreadental_cloud;"', "Creando base de datos kreadental_cloud"):
        print("⚠️ La base de datos ya existe o hay un error de permisos")
    
    return True

def cambiar_a_postgresql():
    """Cambia la configuración a PostgreSQL"""
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

def verificar_migracion_completa():
    """Verifica que la migración completa fue exitosa"""
    print("\n🔍 Verificando migración completa...")
    
    # Verificar que Django funciona
    if not ejecutar_comando("python manage.py check", "Verificando configuración Django"):
        return False
    
    # Verificar tablas en PostgreSQL
    if not ejecutar_comando('psql -U postgres -d kreadental_cloud -c "\\dt"', "Verificando tablas en PostgreSQL"):
        return False
    
    return True

def iniciar_servidor():
    """Inicia el servidor Django"""
    print("\n🚀 Iniciando servidor Django...")
    
    print("✅ Servidor iniciado. Accede a: http://127.0.0.1:8000")
    print("📋 Para detener el servidor presiona Ctrl+C")
    
    # Iniciar servidor en background
    subprocess.Popen(['python', 'manage.py', 'runserver'], shell=True)
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando migración final a PostgreSQL para producción...")
    
    # Paso 1: Exportar datos de SQLite
    if not exportar_datos_sqlite():
        print("❌ No se pudieron exportar los datos de SQLite")
        return
    
    # Paso 2: Configurar PostgreSQL
    if not configurar_postgresql_para_produccion():
        print("❌ No se pudo configurar PostgreSQL")
        return
    
    # Paso 3: Cambiar a PostgreSQL
    if not cambiar_a_postgresql():
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
    
    # Paso 6: Verificar migración completa
    if not verificar_migracion_completa():
        print("❌ La migración no se completó correctamente")
        return
    
    # Paso 7: Iniciar servidor
    if not iniciar_servidor():
        print("❌ No se pudo iniciar el servidor")
        return
    
    print("\n🎉 ¡Migración a PostgreSQL completada exitosamente!")
    print("📋 Tu aplicación está lista para producción con PostgreSQL")
    print("🔗 Accede a: http://127.0.0.1:8000")

if __name__ == "__main__":
    main()










