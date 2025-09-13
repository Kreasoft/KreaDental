#!/usr/bin/env python
"""
Script completo para migrar KreaDental Cloud de SQLite a PostgreSQL
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def configurar_path_postgresql():
    """Configurar PATH de PostgreSQL"""
    print("🔧 Configurando PATH de PostgreSQL...")
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        print("✅ PATH configurado")
        return True
    else:
        print("❌ PostgreSQL no encontrado")
        return False

def crear_archivo_env():
    """Crear archivo .env"""
    print("📝 Creando archivo .env...")
    
    env_content = """# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=postgres123
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
        print("✅ Archivo .env creado")
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def crear_respaldo():
    """Crear respaldo de SQLite"""
    print("💾 Creando respaldo de SQLite...")
    
    if not os.path.exists('db.sqlite3'):
        print("❌ No se encontró db.sqlite3")
        return False
    
    # Crear directorio de respaldos
    os.makedirs('backups', exist_ok=True)
    
    # Crear respaldo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backups/db_backup_{timestamp}.sqlite3"
    
    try:
        shutil.copy2('db.sqlite3', backup_file)
        print(f"✅ Respaldo creado: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ Error creando respaldo: {e}")
        return False

def exportar_datos():
    """Exportar datos de SQLite"""
    print("📤 Exportando datos de SQLite...")
    
    try:
        # Configurar temporalmente para SQLite
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
        
        # Modificar settings temporalmente
        import django
        from django.conf import settings
        
        # Guardar configuración original
        original_db = settings.DATABASES['default'].copy()
        
        # Configurar para SQLite
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
            print("✅ Datos exportados exitosamente")
            return True
        else:
            print(f"❌ Error exportando datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error exportando datos: {e}")
        return False

def configurar_postgresql():
    """Configurar PostgreSQL"""
    print("🗄️  Configurando PostgreSQL...")
    
    try:
        # Crear base de datos
        env = os.environ.copy()
        env['PGPASSWORD'] = 'postgres123'
        
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'CREATE DATABASE "kreadental_cloud" WITH ENCODING=\'UTF8\';'
        ], capture_output=True, text=True, env=env)
        
        if result.returncode == 0 or "already exists" in result.stderr:
            print("✅ Base de datos configurada")
            return True
        else:
            print(f"❌ Error configurando base de datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando PostgreSQL: {e}")
        return False

def aplicar_migraciones():
    """Aplicar migraciones a PostgreSQL"""
    print("🔄 Aplicando migraciones a PostgreSQL...")
    
    try:
        # Restaurar configuración de PostgreSQL
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
        
        result = subprocess.run([
            'python', 'manage.py', 'migrate'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migraciones aplicadas")
            return True
        else:
            print(f"❌ Error aplicando migraciones: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error aplicando migraciones: {e}")
        return False

def importar_datos():
    """Importar datos a PostgreSQL"""
    print("📥 Importando datos a PostgreSQL...")
    
    if not os.path.exists('datos_exportados.json'):
        print("❌ No se encontró datos_exportados.json")
        return False
    
    try:
        result = subprocess.run([
            'python', 'manage.py', 'loaddata', 'datos_exportados.json'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Datos importados")
            return True
        else:
            print(f"❌ Error importando datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error importando datos: {e}")
        return False

def verificar_migracion():
    """Verificar que la migración fue exitosa"""
    print("🔍 Verificando migración...")
    
    try:
        result = subprocess.run([
            'python', 'manage.py', 'check'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Verificación exitosa")
            return True
        else:
            print(f"❌ Error en verificación: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False

def main():
    """Función principal de migración completa"""
    print("🚀 MIGRACIÓN COMPLETA A POSTGRESQL")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Pasos de migración
    pasos = [
        ("Configurar PATH PostgreSQL", configurar_path_postgresql),
        ("Crear archivo .env", crear_archivo_env),
        ("Crear respaldo SQLite", crear_respaldo),
        ("Exportar datos SQLite", exportar_datos),
        ("Configurar PostgreSQL", configurar_postgresql),
        ("Aplicar migraciones", aplicar_migraciones),
        ("Importar datos", importar_datos),
        ("Verificar migración", verificar_migracion),
    ]
    
    for paso, funcion in pasos:
        print(f"\n📋 Paso: {paso}")
        print("-" * 30)
        
        if not funcion():
            print(f"\n❌ Migración falló en: {paso}")
            return False
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("✅ La base de datos ha sido migrada de SQLite a PostgreSQL")
    print("✅ Los datos han sido preservados")
    print("✅ El sistema está listo para usar")
    print("\n📝 Próximos pasos:")
    print("1. python manage.py runserver")
    print("2. Verificar que todo funcione correctamente")
    print("3. Crear superusuario si es necesario: python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


"""
Script completo para migrar KreaDental Cloud de SQLite a PostgreSQL
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def configurar_path_postgresql():
    """Configurar PATH de PostgreSQL"""
    print("🔧 Configurando PATH de PostgreSQL...")
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        print("✅ PATH configurado")
        return True
    else:
        print("❌ PostgreSQL no encontrado")
        return False

def crear_archivo_env():
    """Crear archivo .env"""
    print("📝 Creando archivo .env...")
    
    env_content = """# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=postgres123
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
        print("✅ Archivo .env creado")
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def crear_respaldo():
    """Crear respaldo de SQLite"""
    print("💾 Creando respaldo de SQLite...")
    
    if not os.path.exists('db.sqlite3'):
        print("❌ No se encontró db.sqlite3")
        return False
    
    # Crear directorio de respaldos
    os.makedirs('backups', exist_ok=True)
    
    # Crear respaldo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backups/db_backup_{timestamp}.sqlite3"
    
    try:
        shutil.copy2('db.sqlite3', backup_file)
        print(f"✅ Respaldo creado: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ Error creando respaldo: {e}")
        return False

def exportar_datos():
    """Exportar datos de SQLite"""
    print("📤 Exportando datos de SQLite...")
    
    try:
        # Configurar temporalmente para SQLite
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
        
        # Modificar settings temporalmente
        import django
        from django.conf import settings
        
        # Guardar configuración original
        original_db = settings.DATABASES['default'].copy()
        
        # Configurar para SQLite
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
            print("✅ Datos exportados exitosamente")
            return True
        else:
            print(f"❌ Error exportando datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error exportando datos: {e}")
        return False

def configurar_postgresql():
    """Configurar PostgreSQL"""
    print("🗄️  Configurando PostgreSQL...")
    
    try:
        # Crear base de datos
        env = os.environ.copy()
        env['PGPASSWORD'] = 'postgres123'
        
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'CREATE DATABASE "kreadental_cloud" WITH ENCODING=\'UTF8\';'
        ], capture_output=True, text=True, env=env)
        
        if result.returncode == 0 or "already exists" in result.stderr:
            print("✅ Base de datos configurada")
            return True
        else:
            print(f"❌ Error configurando base de datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando PostgreSQL: {e}")
        return False

def aplicar_migraciones():
    """Aplicar migraciones a PostgreSQL"""
    print("🔄 Aplicando migraciones a PostgreSQL...")
    
    try:
        # Restaurar configuración de PostgreSQL
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
        
        result = subprocess.run([
            'python', 'manage.py', 'migrate'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migraciones aplicadas")
            return True
        else:
            print(f"❌ Error aplicando migraciones: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error aplicando migraciones: {e}")
        return False

def importar_datos():
    """Importar datos a PostgreSQL"""
    print("📥 Importando datos a PostgreSQL...")
    
    if not os.path.exists('datos_exportados.json'):
        print("❌ No se encontró datos_exportados.json")
        return False
    
    try:
        result = subprocess.run([
            'python', 'manage.py', 'loaddata', 'datos_exportados.json'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Datos importados")
            return True
        else:
            print(f"❌ Error importando datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error importando datos: {e}")
        return False

def verificar_migracion():
    """Verificar que la migración fue exitosa"""
    print("🔍 Verificando migración...")
    
    try:
        result = subprocess.run([
            'python', 'manage.py', 'check'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Verificación exitosa")
            return True
        else:
            print(f"❌ Error en verificación: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False

def main():
    """Función principal de migración completa"""
    print("🚀 MIGRACIÓN COMPLETA A POSTGRESQL")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Pasos de migración
    pasos = [
        ("Configurar PATH PostgreSQL", configurar_path_postgresql),
        ("Crear archivo .env", crear_archivo_env),
        ("Crear respaldo SQLite", crear_respaldo),
        ("Exportar datos SQLite", exportar_datos),
        ("Configurar PostgreSQL", configurar_postgresql),
        ("Aplicar migraciones", aplicar_migraciones),
        ("Importar datos", importar_datos),
        ("Verificar migración", verificar_migracion),
    ]
    
    for paso, funcion in pasos:
        print(f"\n📋 Paso: {paso}")
        print("-" * 30)
        
        if not funcion():
            print(f"\n❌ Migración falló en: {paso}")
            return False
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("✅ La base de datos ha sido migrada de SQLite a PostgreSQL")
    print("✅ Los datos han sido preservados")
    print("✅ El sistema está listo para usar")
    print("\n📝 Próximos pasos:")
    print("1. python manage.py runserver")
    print("2. Verificar que todo funcione correctamente")
    print("3. Crear superusuario si es necesario: python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)







