#!/usr/bin/env python
"""
Script para verificar que el sistema esté listo para la migración
"""

import os
import sys
import subprocess
import importlib

def verificar_python():
    """Verificar versión de Python"""
    print("🐍 Verificando Python...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.8+")
        return False

def verificar_django():
    """Verificar Django"""
    print("🌐 Verificando Django...")
    
    try:
        import django
        print(f"✅ Django {django.get_version()} - OK")
        return True
    except ImportError:
        print("❌ Django no está instalado")
        return False

def verificar_postgresql():
    """Verificar PostgreSQL"""
    print("🐘 Verificando PostgreSQL...")
    
    try:
        result = subprocess.run("psql --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL - {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL no está instalado o no está en el PATH")
            return False
    except:
        print("❌ No se pudo verificar PostgreSQL")
        return False

def verificar_psycopg2():
    """Verificar psycopg2"""
    print("🔌 Verificando psycopg2...")
    
    try:
        import psycopg2
        print(f"✅ psycopg2 {psycopg2.__version__} - OK")
        return True
    except ImportError:
        print("❌ psycopg2 no está instalado")
        return False

def verificar_dotenv():
    """Verificar python-dotenv"""
    print("🔧 Verificando python-dotenv...")
    
    try:
        import dotenv
        # dotenv no siempre tiene __version__, verificar de otra manera
        print("✅ python-dotenv - OK")
        return True
    except ImportError:
        print("❌ python-dotenv no está instalado")
        return False

def verificar_archivos():
    """Verificar archivos del proyecto"""
    print("📁 Verificando archivos del proyecto...")
    
    archivos_requeridos = [
        'manage.py',
        'config/settings.py',
        'requirements.txt',
        'db.sqlite3'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print("❌ Archivos faltantes:")
        for archivo in archivos_faltantes:
            print(f"   - {archivo}")
        return False
    else:
        print("✅ Todos los archivos requeridos están presentes")
        return True

def verificar_archivo_env():
    """Verificar archivo .env"""
    print("🔐 Verificando archivo .env...")
    
    if not os.path.exists('.env'):
        print("⚠️  Archivo .env no encontrado")
        print("   Ejecuta: python configurar_postgresql.py")
        return False
    
    # Verificar variables requeridas
    from dotenv import load_dotenv
    load_dotenv()
    
    variables_requeridas = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    variables_faltantes = []
    
    for var in variables_requeridas:
        if not os.getenv(var):
            variables_faltantes.append(var)
    
    if variables_faltantes:
        print("❌ Variables faltantes en .env:")
        for var in variables_faltantes:
            print(f"   - {var}")
        return False
    else:
        print("✅ Archivo .env configurado correctamente")
        return True

def verificar_conexion_postgresql():
    """Verificar conexión a PostgreSQL"""
    print("🔗 Verificando conexión a PostgreSQL...")
    
    try:
        import psycopg2
        from dotenv import load_dotenv
        
        load_dotenv()
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': 'postgres'
        }
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Conexión exitosa a PostgreSQL")
        print(f"   📊 {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def verificar_django_settings():
    """Verificar configuración de Django"""
    print("⚙️  Verificando configuración de Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Verificar que la base de datos esté configurada para PostgreSQL
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in db_engine:
            print("✅ Django configurado para PostgreSQL")
            return True
        else:
            print(f"⚠️  Django configurado para {db_engine}")
            print("   La migración cambiará esto a PostgreSQL")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando Django: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICACIÓN DEL SISTEMA")
    print("=" * 40)
    print("KreaDental Cloud - Migración a PostgreSQL")
    print("=" * 40)
    
    verificaciones = [
        ("Python", verificar_python),
        ("Django", verificar_django),
        ("PostgreSQL", verificar_postgresql),
        ("psycopg2", verificar_psycopg2),
        ("python-dotenv", verificar_dotenv),
        ("Archivos del proyecto", verificar_archivos),
        ("Archivo .env", verificar_archivo_env),
        ("Conexión PostgreSQL", verificar_conexion_postgresql),
        ("Configuración Django", verificar_django_settings),
    ]
    
    resultados = []
    
    for nombre, funcion in verificaciones:
        print(f"\n📋 {nombre}:")
        print("-" * 20)
        resultado = funcion()
        resultados.append(resultado)
    
    # Resumen
    print("\n" + "=" * 40)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 40)
    
    exitosos = sum(resultados)
    total = len(resultados)
    
    if exitosos == total:
        print("🎉 ¡TODAS LAS VERIFICACIONES EXITOSAS!")
        print("✅ El sistema está listo para la migración")
        print("\n📝 Próximos pasos:")
        print("   1. python migrate_to_postgresql.py")
        print("   2. python manage.py runserver")
    else:
        print(f"⚠️  {exitosos}/{total} verificaciones exitosas")
        print("❌ Hay problemas que resolver antes de la migración")
        print("\n💡 Soluciones:")
        print("   - Instalar dependencias faltantes: pip install -r requirements.txt")
        print("   - Configurar PostgreSQL: python configurar_postgresql.py")
        print("   - Verificar que PostgreSQL esté ejecutándose")
    
    return exitosos == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

Script para verificar que el sistema esté listo para la migración
"""

import os
import sys
import subprocess
import importlib

def verificar_python():
    """Verificar versión de Python"""
    print("🐍 Verificando Python...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.8+")
        return False

def verificar_django():
    """Verificar Django"""
    print("🌐 Verificando Django...")
    
    try:
        import django
        print(f"✅ Django {django.get_version()} - OK")
        return True
    except ImportError:
        print("❌ Django no está instalado")
        return False

def verificar_postgresql():
    """Verificar PostgreSQL"""
    print("🐘 Verificando PostgreSQL...")
    
    try:
        result = subprocess.run("psql --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL - {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL no está instalado o no está en el PATH")
            return False
    except:
        print("❌ No se pudo verificar PostgreSQL")
        return False

def verificar_psycopg2():
    """Verificar psycopg2"""
    print("🔌 Verificando psycopg2...")
    
    try:
        import psycopg2
        print(f"✅ psycopg2 {psycopg2.__version__} - OK")
        return True
    except ImportError:
        print("❌ psycopg2 no está instalado")
        return False

def verificar_dotenv():
    """Verificar python-dotenv"""
    print("🔧 Verificando python-dotenv...")
    
    try:
        import dotenv
        # dotenv no siempre tiene __version__, verificar de otra manera
        print("✅ python-dotenv - OK")
        return True
    except ImportError:
        print("❌ python-dotenv no está instalado")
        return False

def verificar_archivos():
    """Verificar archivos del proyecto"""
    print("📁 Verificando archivos del proyecto...")
    
    archivos_requeridos = [
        'manage.py',
        'config/settings.py',
        'requirements.txt',
        'db.sqlite3'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print("❌ Archivos faltantes:")
        for archivo in archivos_faltantes:
            print(f"   - {archivo}")
        return False
    else:
        print("✅ Todos los archivos requeridos están presentes")
        return True

def verificar_archivo_env():
    """Verificar archivo .env"""
    print("🔐 Verificando archivo .env...")
    
    if not os.path.exists('.env'):
        print("⚠️  Archivo .env no encontrado")
        print("   Ejecuta: python configurar_postgresql.py")
        return False
    
    # Verificar variables requeridas
    from dotenv import load_dotenv
    load_dotenv()
    
    variables_requeridas = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    variables_faltantes = []
    
    for var in variables_requeridas:
        if not os.getenv(var):
            variables_faltantes.append(var)
    
    if variables_faltantes:
        print("❌ Variables faltantes en .env:")
        for var in variables_faltantes:
            print(f"   - {var}")
        return False
    else:
        print("✅ Archivo .env configurado correctamente")
        return True

def verificar_conexion_postgresql():
    """Verificar conexión a PostgreSQL"""
    print("🔗 Verificando conexión a PostgreSQL...")
    
    try:
        import psycopg2
        from dotenv import load_dotenv
        
        load_dotenv()
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': 'postgres'
        }
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Conexión exitosa a PostgreSQL")
        print(f"   📊 {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def verificar_django_settings():
    """Verificar configuración de Django"""
    print("⚙️  Verificando configuración de Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Verificar que la base de datos esté configurada para PostgreSQL
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in db_engine:
            print("✅ Django configurado para PostgreSQL")
            return True
        else:
            print(f"⚠️  Django configurado para {db_engine}")
            print("   La migración cambiará esto a PostgreSQL")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando Django: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICACIÓN DEL SISTEMA")
    print("=" * 40)
    print("KreaDental Cloud - Migración a PostgreSQL")
    print("=" * 40)
    
    verificaciones = [
        ("Python", verificar_python),
        ("Django", verificar_django),
        ("PostgreSQL", verificar_postgresql),
        ("psycopg2", verificar_psycopg2),
        ("python-dotenv", verificar_dotenv),
        ("Archivos del proyecto", verificar_archivos),
        ("Archivo .env", verificar_archivo_env),
        ("Conexión PostgreSQL", verificar_conexion_postgresql),
        ("Configuración Django", verificar_django_settings),
    ]
    
    resultados = []
    
    for nombre, funcion in verificaciones:
        print(f"\n📋 {nombre}:")
        print("-" * 20)
        resultado = funcion()
        resultados.append(resultado)
    
    # Resumen
    print("\n" + "=" * 40)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 40)
    
    exitosos = sum(resultados)
    total = len(resultados)
    
    if exitosos == total:
        print("🎉 ¡TODAS LAS VERIFICACIONES EXITOSAS!")
        print("✅ El sistema está listo para la migración")
        print("\n📝 Próximos pasos:")
        print("   1. python migrate_to_postgresql.py")
        print("   2. python manage.py runserver")
    else:
        print(f"⚠️  {exitosos}/{total} verificaciones exitosas")
        print("❌ Hay problemas que resolver antes de la migración")
        print("\n💡 Soluciones:")
        print("   - Instalar dependencias faltantes: pip install -r requirements.txt")
        print("   - Configurar PostgreSQL: python configurar_postgresql.py")
        print("   - Verificar que PostgreSQL esté ejecutándose")
    
    return exitosos == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
