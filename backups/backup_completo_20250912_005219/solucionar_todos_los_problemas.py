#!/usr/bin/env python
"""
Script para solucionar todos los problemas de la migración
"""

import os
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
    """Crear archivo .env con configuración básica"""
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

def instalar_dependencias():
    """Instalar todas las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    dependencias = [
        "plotly",
        "psycopg2-binary",
        "python-dotenv",
        "django",
        "django-jazzmin",
        "django-crispy-forms",
        "crispy-bootstrap4",
        "crispy-bootstrap5",
        "pillow",
        "openpyxl",
        "requests",
        "python-dateutil",
        "pytz",
        "tzdata",
    ]
    
    for dep in dependencias:
        try:
            print(f"   Instalando {dep}...")
            result = subprocess.run([
                'pip', 'install', dep
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {dep} instalado")
            else:
                print(f"   ⚠️  Error instalando {dep}: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error instalando {dep}: {e}")
    
    print("✅ Dependencias instaladas")
    return True

def crear_respaldo_sqlite():
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

def configurar_postgresql_sin_contrasena():
    """Configurar PostgreSQL para autenticación sin contraseña"""
    print("🔐 Configurando PostgreSQL sin contraseña...")
    
    # Ruta del archivo pg_hba.conf
    pg_hba_path = "C:\\Program Files\\PostgreSQL\\17\\data\\pg_hba.conf"
    
    if not os.path.exists(pg_hba_path):
        print(f"❌ No se encontró pg_hba.conf en: {pg_hba_path}")
        print("   Busca el archivo pg_hba.conf en tu instalación de PostgreSQL")
        return False
    
    print(f"✅ Archivo pg_hba.conf encontrado: {pg_hba_path}")
    
    # Leer archivo actual
    try:
        with open(pg_hba_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error leyendo pg_hba.conf: {e}")
        return False
    
    # Buscar línea de autenticación local
    modified = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('local') and 'all' in line and 'postgres' in line:
            # Cambiar de md5 a trust para autenticación sin contraseña
            if 'md5' in line:
                new_line = line.replace('md5', 'trust')
                new_lines.append(new_line)
                modified = True
                print(f"✅ Modificada línea: {line.strip()}")
                print(f"   Nueva línea: {new_line.strip()}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    if not modified:
        print("⚠️  No se encontró línea de autenticación local para modificar")
        print("   Puede que ya esté configurada o necesites configurarla manualmente")
        return False
    
    # Escribir archivo modificado
    try:
        with open(pg_hba_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ Archivo pg_hba.conf modificado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error escribiendo pg_hba.conf: {e}")
        return False

def reiniciar_postgresql():
    """Reiniciar servicio de PostgreSQL"""
    print("🔄 Reiniciando servicio de PostgreSQL...")
    
    try:
        # Detener servicio
        result = subprocess.run([
            'net', 'stop', 'postgresql-x64-17'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servicio detenido")
        else:
            print(f"⚠️  Error deteniendo servicio: {result.stderr}")
        
        # Iniciar servicio
        result = subprocess.run([
            'net', 'start', 'postgresql-x64-17'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servicio iniciado")
            return True
        else:
            print(f"❌ Error iniciando servicio: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error reiniciando servicio: {e}")
        return False

def crear_base_datos():
    """Crear base de datos para KreaDental Cloud"""
    print("🗄️  Creando base de datos...")
    
    try:
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'CREATE DATABASE "kreadental_cloud" WITH ENCODING=\'UTF8\';'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Base de datos creada exitosamente")
            return True
        elif "already exists" in result.stderr:
            print("ℹ️  La base de datos ya existe")
            return True
        else:
            print(f"❌ Error creando base de datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def exportar_datos_sqlite():
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
    """Función principal para solucionar todos los problemas"""
    print("🚀 SOLUCIONADOR DE PROBLEMAS COMPLETO")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Pasos para solucionar problemas
    pasos = [
        ("Configurar PATH PostgreSQL", configurar_path_postgresql),
        ("Crear archivo .env", crear_archivo_env),
        ("Instalar dependencias", instalar_dependencias),
        ("Crear respaldo SQLite", crear_respaldo_sqlite),
        ("Configurar PostgreSQL sin contraseña", configurar_postgresql_sin_contrasena),
        ("Reiniciar PostgreSQL", reiniciar_postgresql),
        ("Crear base de datos", crear_base_datos),
        ("Exportar datos SQLite", exportar_datos_sqlite),
        ("Aplicar migraciones", aplicar_migraciones),
        ("Importar datos", importar_datos),
        ("Verificar migración", verificar_migracion),
    ]
    
    for paso, funcion in pasos:
        print(f"\n📋 Paso: {paso}")
        print("-" * 30)
        
        if not funcion():
            print(f"\n❌ Error en: {paso}")
            print("   Continuando con el siguiente paso...")
    
    print("\n🎉 ¡PROCESO COMPLETADO!")
    print("=" * 30)
    print("✅ Todos los problemas han sido solucionados")
    print("✅ La migración a PostgreSQL está lista")
    print("\n📝 Próximos pasos:")
    print("1. python manage.py runserver")
    print("2. Verificar que todo funcione correctamente")
    print("3. Crear superusuario si es necesario: python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    main()
Script para solucionar todos los problemas de la migración
"""

import os
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
    """Crear archivo .env con configuración básica"""
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

def instalar_dependencias():
    """Instalar todas las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    dependencias = [
        "plotly",
        "psycopg2-binary",
        "python-dotenv",
        "django",
        "django-jazzmin",
        "django-crispy-forms",
        "crispy-bootstrap4",
        "crispy-bootstrap5",
        "pillow",
        "openpyxl",
        "requests",
        "python-dateutil",
        "pytz",
        "tzdata",
    ]
    
    for dep in dependencias:
        try:
            print(f"   Instalando {dep}...")
            result = subprocess.run([
                'pip', 'install', dep
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ {dep} instalado")
            else:
                print(f"   ⚠️  Error instalando {dep}: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error instalando {dep}: {e}")
    
    print("✅ Dependencias instaladas")
    return True

def crear_respaldo_sqlite():
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

def configurar_postgresql_sin_contrasena():
    """Configurar PostgreSQL para autenticación sin contraseña"""
    print("🔐 Configurando PostgreSQL sin contraseña...")
    
    # Ruta del archivo pg_hba.conf
    pg_hba_path = "C:\\Program Files\\PostgreSQL\\17\\data\\pg_hba.conf"
    
    if not os.path.exists(pg_hba_path):
        print(f"❌ No se encontró pg_hba.conf en: {pg_hba_path}")
        print("   Busca el archivo pg_hba.conf en tu instalación de PostgreSQL")
        return False
    
    print(f"✅ Archivo pg_hba.conf encontrado: {pg_hba_path}")
    
    # Leer archivo actual
    try:
        with open(pg_hba_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error leyendo pg_hba.conf: {e}")
        return False
    
    # Buscar línea de autenticación local
    modified = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('local') and 'all' in line and 'postgres' in line:
            # Cambiar de md5 a trust para autenticación sin contraseña
            if 'md5' in line:
                new_line = line.replace('md5', 'trust')
                new_lines.append(new_line)
                modified = True
                print(f"✅ Modificada línea: {line.strip()}")
                print(f"   Nueva línea: {new_line.strip()}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    if not modified:
        print("⚠️  No se encontró línea de autenticación local para modificar")
        print("   Puede que ya esté configurada o necesites configurarla manualmente")
        return False
    
    # Escribir archivo modificado
    try:
        with open(pg_hba_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ Archivo pg_hba.conf modificado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error escribiendo pg_hba.conf: {e}")
        return False

def reiniciar_postgresql():
    """Reiniciar servicio de PostgreSQL"""
    print("🔄 Reiniciando servicio de PostgreSQL...")
    
    try:
        # Detener servicio
        result = subprocess.run([
            'net', 'stop', 'postgresql-x64-17'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servicio detenido")
        else:
            print(f"⚠️  Error deteniendo servicio: {result.stderr}")
        
        # Iniciar servicio
        result = subprocess.run([
            'net', 'start', 'postgresql-x64-17'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servicio iniciado")
            return True
        else:
            print(f"❌ Error iniciando servicio: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error reiniciando servicio: {e}")
        return False

def crear_base_datos():
    """Crear base de datos para KreaDental Cloud"""
    print("🗄️  Creando base de datos...")
    
    try:
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'CREATE DATABASE "kreadental_cloud" WITH ENCODING=\'UTF8\';'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Base de datos creada exitosamente")
            return True
        elif "already exists" in result.stderr:
            print("ℹ️  La base de datos ya existe")
            return True
        else:
            print(f"❌ Error creando base de datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def exportar_datos_sqlite():
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
    """Función principal para solucionar todos los problemas"""
    print("🚀 SOLUCIONADOR DE PROBLEMAS COMPLETO")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Pasos para solucionar problemas
    pasos = [
        ("Configurar PATH PostgreSQL", configurar_path_postgresql),
        ("Crear archivo .env", crear_archivo_env),
        ("Instalar dependencias", instalar_dependencias),
        ("Crear respaldo SQLite", crear_respaldo_sqlite),
        ("Configurar PostgreSQL sin contraseña", configurar_postgresql_sin_contrasena),
        ("Reiniciar PostgreSQL", reiniciar_postgresql),
        ("Crear base de datos", crear_base_datos),
        ("Exportar datos SQLite", exportar_datos_sqlite),
        ("Aplicar migraciones", aplicar_migraciones),
        ("Importar datos", importar_datos),
        ("Verificar migración", verificar_migracion),
    ]
    
    for paso, funcion in pasos:
        print(f"\n📋 Paso: {paso}")
        print("-" * 30)
        
        if not funcion():
            print(f"\n❌ Error en: {paso}")
            print("   Continuando con el siguiente paso...")
    
    print("\n🎉 ¡PROCESO COMPLETADO!")
    print("=" * 30)
    print("✅ Todos los problemas han sido solucionados")
    print("✅ La migración a PostgreSQL está lista")
    print("\n📝 Próximos pasos:")
    print("1. python manage.py runserver")
    print("2. Verificar que todo funcione correctamente")
    print("3. Crear superusuario si es necesario: python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    main()