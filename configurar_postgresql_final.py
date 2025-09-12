#!/usr/bin/env python
"""
Script para configurar PostgreSQL y migrar desde SQLite
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
            if resultado.stdout:
                print(f"Salida: {resultado.stdout}")
        else:
            print(f"❌ {descripcion} - Error")
            if resultado.stderr:
                print(f"Error: {resultado.stderr}")
        return resultado.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def crear_archivo_env():
    """Crea el archivo .env con la configuración de PostgreSQL"""
    print("\n📝 Creando archivo .env...")
    
    # Intentar crear .env directamente
    env_content = """# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Configuración de Django
SECRET_KEY=kreasoft-52432cl+
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env creado exitosamente")
        return True
    except Exception as e:
        print(f"❌ No se pudo crear .env: {e}")
        print("📋 Por favor, crea manualmente el archivo .env con este contenido:")
        print(env_content)
        return False

def configurar_postgresql():
    """Configura PostgreSQL para la migración"""
    print("\n🐘 Configurando PostgreSQL...")
    
    # Verificar si PostgreSQL está instalado
    if not ejecutar_comando("psql --version", "Verificando instalación de PostgreSQL"):
        print("❌ PostgreSQL no está instalado o no está en el PATH")
        print("📋 Instrucciones:")
        print("1. Descarga PostgreSQL desde: https://www.postgresql.org/download/windows/")
        print("2. Instálalo con la contraseña 'postgres' para el usuario postgres")
        print("3. Añade C:\\Program Files\\PostgreSQL\\17\\bin al PATH del sistema")
        return False
    
    # Crear base de datos
    print("\n🗄️ Creando base de datos...")
    comando_crear_db = 'psql -U postgres -c "CREATE DATABASE kreadental_cloud;"'
    if not ejecutar_comando(comando_crear_db, "Creando base de datos kreadental_cloud"):
        print("⚠️ La base de datos ya existe o hay un error de permisos")
    
    return True

def cambiar_a_postgresql():
    """Cambia la configuración de Django a PostgreSQL"""
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
        'NAME': os.getenv('DB_NAME', 'kreadental_cloud'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
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

def hacer_backup_sqlite():
    """Hace backup de la base de datos SQLite"""
    print("\n💾 Haciendo backup de SQLite...")
    
    if os.path.exists('db.sqlite3'):
        backup_file = f"backup_sqlite_{Path().cwd().name}_{subprocess.run('date /t', shell=True, capture_output=True, text=True).stdout.strip().replace('/', '')}.db"
        try:
            import shutil
            shutil.copy2('db.sqlite3', backup_file)
            print(f"✅ Backup creado: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
            return False
    else:
        print("⚠️ No se encontró db.sqlite3")
        return False

def exportar_datos():
    """Exporta datos de SQLite"""
    print("\n📤 Exportando datos de SQLite...")
    
    # Cambiar temporalmente a SQLite para exportar
    if not cambiar_a_sqlite_temporal():
        return False
    
    # Exportar datos
    if not ejecutar_comando("python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json", "Exportando datos"):
        print("❌ Error exportando datos")
        return False
    
    print("✅ Datos exportados a datos_exportados.json")
    return True

def cambiar_a_sqlite_temporal():
    """Cambia temporalmente a SQLite para exportar datos"""
    settings_file = "config/settings.py"
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar configuración de base de datos
        old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'kreadental_cloud'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}"""
        
        new_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
        
        content = content.replace(old_config, new_config)
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"❌ Error cambiando a SQLite temporal: {e}")
        return False

def aplicar_migraciones():
    """Aplica migraciones a PostgreSQL"""
    print("\n🔄 Aplicando migraciones a PostgreSQL...")
    
    if not ejecutar_comando("python manage.py migrate", "Aplicando migraciones"):
        return False
    
    return True

def importar_datos():
    """Importa datos a PostgreSQL"""
    print("\n📥 Importando datos a PostgreSQL...")
    
    if not ejecutar_comando("python manage.py loaddata datos_exportados.json", "Importando datos"):
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando migración de SQLite a PostgreSQL...")
    
    # Paso 1: Crear archivo .env
    if not crear_archivo_env():
        print("⚠️ Continuando sin archivo .env...")
    
    # Paso 2: Configurar PostgreSQL
    if not configurar_postgresql():
        print("❌ No se pudo configurar PostgreSQL")
        return
    
    # Paso 3: Hacer backup
    hacer_backup_sqlite()
    
    # Paso 4: Exportar datos
    if not exportar_datos():
        print("❌ No se pudieron exportar los datos")
        return
    
    # Paso 5: Cambiar a PostgreSQL
    if not cambiar_a_postgresql():
        print("❌ No se pudo cambiar a PostgreSQL")
        return
    
    # Paso 6: Aplicar migraciones
    if not aplicar_migraciones():
        print("❌ No se pudieron aplicar las migraciones")
        return
    
    # Paso 7: Importar datos
    if not importar_datos():
        print("❌ No se pudieron importar los datos")
        return
    
    print("\n🎉 ¡Migración completada exitosamente!")
    print("📋 Próximos pasos:")
    print("1. Verifica que la aplicación funciona: python manage.py runserver")
    print("2. Prueba la funcionalidad en el navegador")
    print("3. Si todo funciona bien, puedes eliminar db.sqlite3")

if __name__ == "__main__":
    main()

"""
Script para configurar PostgreSQL y migrar desde SQLite
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
            if resultado.stdout:
                print(f"Salida: {resultado.stdout}")
        else:
            print(f"❌ {descripcion} - Error")
            if resultado.stderr:
                print(f"Error: {resultado.stderr}")
        return resultado.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def crear_archivo_env():
    """Crea el archivo .env con la configuración de PostgreSQL"""
    print("\n📝 Creando archivo .env...")
    
    # Intentar crear .env directamente
    env_content = """# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Configuración de Django
SECRET_KEY=kreasoft-52432cl+
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env creado exitosamente")
        return True
    except Exception as e:
        print(f"❌ No se pudo crear .env: {e}")
        print("📋 Por favor, crea manualmente el archivo .env con este contenido:")
        print(env_content)
        return False

def configurar_postgresql():
    """Configura PostgreSQL para la migración"""
    print("\n🐘 Configurando PostgreSQL...")
    
    # Verificar si PostgreSQL está instalado
    if not ejecutar_comando("psql --version", "Verificando instalación de PostgreSQL"):
        print("❌ PostgreSQL no está instalado o no está en el PATH")
        print("📋 Instrucciones:")
        print("1. Descarga PostgreSQL desde: https://www.postgresql.org/download/windows/")
        print("2. Instálalo con la contraseña 'postgres' para el usuario postgres")
        print("3. Añade C:\\Program Files\\PostgreSQL\\17\\bin al PATH del sistema")
        return False
    
    # Crear base de datos
    print("\n🗄️ Creando base de datos...")
    comando_crear_db = 'psql -U postgres -c "CREATE DATABASE kreadental_cloud;"'
    if not ejecutar_comando(comando_crear_db, "Creando base de datos kreadental_cloud"):
        print("⚠️ La base de datos ya existe o hay un error de permisos")
    
    return True

def cambiar_a_postgresql():
    """Cambia la configuración de Django a PostgreSQL"""
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
        'NAME': os.getenv('DB_NAME', 'kreadental_cloud'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
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

def hacer_backup_sqlite():
    """Hace backup de la base de datos SQLite"""
    print("\n💾 Haciendo backup de SQLite...")
    
    if os.path.exists('db.sqlite3'):
        backup_file = f"backup_sqlite_{Path().cwd().name}_{subprocess.run('date /t', shell=True, capture_output=True, text=True).stdout.strip().replace('/', '')}.db"
        try:
            import shutil
            shutil.copy2('db.sqlite3', backup_file)
            print(f"✅ Backup creado: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
            return False
    else:
        print("⚠️ No se encontró db.sqlite3")
        return False

def exportar_datos():
    """Exporta datos de SQLite"""
    print("\n📤 Exportando datos de SQLite...")
    
    # Cambiar temporalmente a SQLite para exportar
    if not cambiar_a_sqlite_temporal():
        return False
    
    # Exportar datos
    if not ejecutar_comando("python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json", "Exportando datos"):
        print("❌ Error exportando datos")
        return False
    
    print("✅ Datos exportados a datos_exportados.json")
    return True

def cambiar_a_sqlite_temporal():
    """Cambia temporalmente a SQLite para exportar datos"""
    settings_file = "config/settings.py"
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar configuración de base de datos
        old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'kreadental_cloud'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}"""
        
        new_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
        
        content = content.replace(old_config, new_config)
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"❌ Error cambiando a SQLite temporal: {e}")
        return False

def aplicar_migraciones():
    """Aplica migraciones a PostgreSQL"""
    print("\n🔄 Aplicando migraciones a PostgreSQL...")
    
    if not ejecutar_comando("python manage.py migrate", "Aplicando migraciones"):
        return False
    
    return True

def importar_datos():
    """Importa datos a PostgreSQL"""
    print("\n📥 Importando datos a PostgreSQL...")
    
    if not ejecutar_comando("python manage.py loaddata datos_exportados.json", "Importando datos"):
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Iniciando migración de SQLite a PostgreSQL...")
    
    # Paso 1: Crear archivo .env
    if not crear_archivo_env():
        print("⚠️ Continuando sin archivo .env...")
    
    # Paso 2: Configurar PostgreSQL
    if not configurar_postgresql():
        print("❌ No se pudo configurar PostgreSQL")
        return
    
    # Paso 3: Hacer backup
    hacer_backup_sqlite()
    
    # Paso 4: Exportar datos
    if not exportar_datos():
        print("❌ No se pudieron exportar los datos")
        return
    
    # Paso 5: Cambiar a PostgreSQL
    if not cambiar_a_postgresql():
        print("❌ No se pudo cambiar a PostgreSQL")
        return
    
    # Paso 6: Aplicar migraciones
    if not aplicar_migraciones():
        print("❌ No se pudieron aplicar las migraciones")
        return
    
    # Paso 7: Importar datos
    if not importar_datos():
        print("❌ No se pudieron importar los datos")
        return
    
    print("\n🎉 ¡Migración completada exitosamente!")
    print("📋 Próximos pasos:")
    print("1. Verifica que la aplicación funciona: python manage.py runserver")
    print("2. Prueba la funcionalidad en el navegador")
    print("3. Si todo funciona bien, puedes eliminar db.sqlite3")

if __name__ == "__main__":
    main()




