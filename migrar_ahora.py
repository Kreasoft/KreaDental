#!/usr/bin/env python
"""
Script simple para migrar a PostgreSQL
"""

import os
import subprocess

def configurar_path():
    """Configurar PATH de PostgreSQL"""
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        return True
    return False

def crear_env():
    """Crear archivo .env"""
    env_content = """DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=kreasoft-52432cl+
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Archivo .env creado")

def crear_respaldo():
    """Crear respaldo de SQLite"""
    import shutil
    from datetime import datetime
    
    os.makedirs('backups', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backups/db_backup_{timestamp}.sqlite3"
    
    shutil.copy2('db.sqlite3', backup_file)
    print(f"✅ Respaldo creado: {backup_file}")

def exportar_datos():
    """Exportar datos de SQLite"""
    # Configurar para SQLite temporalmente
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    
    # Modificar settings para SQLite
    import django
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
    django.setup()
    
    # Exportar datos
    result = subprocess.run([
        'python', 'manage.py', 'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '-e', 'contenttypes',
        '-e', 'auth.Permission',
        '-e', 'sessions',
        '--output', 'datos_exportados.json'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Datos exportados")
    else:
        print(f"❌ Error exportando: {result.stderr}")

def configurar_postgresql():
    """Configurar PostgreSQL"""
    env = os.environ.copy()
    env['PGPASSWORD'] = 'postgres123'
    
    result = subprocess.run([
        'psql', '-U', 'postgres', '-d', 'postgres',
        '-c', 'CREATE DATABASE "kreadental_cloud" WITH ENCODING=\'UTF8\';'
    ], capture_output=True, text=True, env=env)
    
    if result.returncode == 0 or "already exists" in result.stderr:
        print("✅ Base de datos configurada")
    else:
        print(f"❌ Error configurando: {result.stderr}")

def aplicar_migraciones():
    """Aplicar migraciones"""
    result = subprocess.run([
        'python', 'manage.py', 'migrate'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Migraciones aplicadas")
    else:
        print(f"❌ Error migraciones: {result.stderr}")

def importar_datos():
    """Importar datos"""
    result = subprocess.run([
        'python', 'manage.py', 'loaddata', 'datos_exportados.json'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Datos importados")
    else:
        print(f"❌ Error importando: {result.stderr}")

def main():
    print("🚀 MIGRACIÓN A POSTGRESQL")
    print("=" * 30)
    
    # Configurar PATH
    configurar_path()
    
    # Crear .env
    crear_env()
    
    # Crear respaldo
    crear_respaldo()
    
    # Exportar datos
    exportar_datos()
    
    # Configurar PostgreSQL
    configurar_postgresql()
    
    # Aplicar migraciones
    aplicar_migraciones()
    
    # Importar datos
    importar_datos()
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA!")
    print("Ejecuta: python manage.py runserver")

if __name__ == "__main__":
    main()


"""
Script simple para migrar a PostgreSQL
"""

import os
import subprocess

def configurar_path():
    """Configurar PATH de PostgreSQL"""
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        return True
    return False

def crear_env():
    """Crear archivo .env"""
    env_content = """DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=kreasoft-52432cl+
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Archivo .env creado")

def crear_respaldo():
    """Crear respaldo de SQLite"""
    import shutil
    from datetime import datetime
    
    os.makedirs('backups', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backups/db_backup_{timestamp}.sqlite3"
    
    shutil.copy2('db.sqlite3', backup_file)
    print(f"✅ Respaldo creado: {backup_file}")

def exportar_datos():
    """Exportar datos de SQLite"""
    # Configurar para SQLite temporalmente
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    
    # Modificar settings para SQLite
    import django
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
    django.setup()
    
    # Exportar datos
    result = subprocess.run([
        'python', 'manage.py', 'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '-e', 'contenttypes',
        '-e', 'auth.Permission',
        '-e', 'sessions',
        '--output', 'datos_exportados.json'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Datos exportados")
    else:
        print(f"❌ Error exportando: {result.stderr}")

def configurar_postgresql():
    """Configurar PostgreSQL"""
    env = os.environ.copy()
    env['PGPASSWORD'] = 'postgres123'
    
    result = subprocess.run([
        'psql', '-U', 'postgres', '-d', 'postgres',
        '-c', 'CREATE DATABASE "kreadental_cloud" WITH ENCODING=\'UTF8\';'
    ], capture_output=True, text=True, env=env)
    
    if result.returncode == 0 or "already exists" in result.stderr:
        print("✅ Base de datos configurada")
    else:
        print(f"❌ Error configurando: {result.stderr}")

def aplicar_migraciones():
    """Aplicar migraciones"""
    result = subprocess.run([
        'python', 'manage.py', 'migrate'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Migraciones aplicadas")
    else:
        print(f"❌ Error migraciones: {result.stderr}")

def importar_datos():
    """Importar datos"""
    result = subprocess.run([
        'python', 'manage.py', 'loaddata', 'datos_exportados.json'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Datos importados")
    else:
        print(f"❌ Error importando: {result.stderr}")

def main():
    print("🚀 MIGRACIÓN A POSTGRESQL")
    print("=" * 30)
    
    # Configurar PATH
    configurar_path()
    
    # Crear .env
    crear_env()
    
    # Crear respaldo
    crear_respaldo()
    
    # Exportar datos
    exportar_datos()
    
    # Configurar PostgreSQL
    configurar_postgresql()
    
    # Aplicar migraciones
    aplicar_migraciones()
    
    # Importar datos
    importar_datos()
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA!")
    print("Ejecuta: python manage.py runserver")

if __name__ == "__main__":
    main()





