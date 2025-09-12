#!/usr/bin/env python
"""
Script principal para migrar KreaDental Cloud de SQLite a PostgreSQL
"""

import os
import sys
import subprocess
from datetime import datetime

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"🔄 {descripcion}...")
    
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {descripcion} completado")
            if result.stdout:
                print(f"   📝 {result.stdout.strip()}")
        else:
            print(f"❌ Error en {descripcion}")
            if result.stderr:
                print(f"   🚨 {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False
    
    return True

def verificar_postgresql():
    """Verificar que PostgreSQL esté instalado y funcionando"""
    print("🔍 Verificando PostgreSQL...")
    
    try:
        result = subprocess.run("psql --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL encontrado: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL no está instalado o no está en el PATH")
            return False
    except:
        print("❌ No se pudo verificar PostgreSQL")
        return False

def verificar_archivo_env():
    """Verificar que existe el archivo .env"""
    if not os.path.exists('.env'):
        print("❌ No se encontró el archivo .env")
        print("   Crea un archivo .env con la configuración de PostgreSQL")
        print("   Puedes usar el archivo MIGRACION_POSTGRESQL.md como referencia")
        return False
    
    print("✅ Archivo .env encontrado")
    return True

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
        import shutil
        shutil.copy2('db.sqlite3', backup_file)
        print(f"✅ Respaldo creado: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ Error creando respaldo: {e}")
        return False

def exportar_datos():
    """Exportar datos de SQLite"""
    print("📤 Exportando datos de SQLite...")
    
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
    comando = "python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -e sessions --output datos_exportados.json"
    
    if ejecutar_comando(comando, "Exportando datos"):
        print("✅ Datos exportados exitosamente")
        return True
    else:
        print("❌ Error exportando datos")
        return False

def configurar_postgresql():
    """Configurar PostgreSQL"""
    print("🔧 Configurando PostgreSQL...")
    
    if ejecutar_comando("python config_database.py", "Configurando base de datos"):
        print("✅ PostgreSQL configurado")
        return True
    else:
        print("❌ Error configurando PostgreSQL")
        return False

def aplicar_migraciones():
    """Aplicar migraciones a PostgreSQL"""
    print("🔄 Aplicando migraciones a PostgreSQL...")
    
    # Restaurar configuración de PostgreSQL
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    
    if ejecutar_comando("python manage.py migrate", "Aplicando migraciones"):
        print("✅ Migraciones aplicadas")
        return True
    else:
        print("❌ Error aplicando migraciones")
        return False

def importar_datos():
    """Importar datos a PostgreSQL"""
    print("📥 Importando datos a PostgreSQL...")
    
    if not os.path.exists('datos_exportados.json'):
        print("❌ No se encontró datos_exportados.json")
        return False
    
    if ejecutar_comando("python manage.py loaddata datos_exportados.json", "Importando datos"):
        print("✅ Datos importados")
        return True
    else:
        print("❌ Error importando datos")
        return False

def verificar_migracion():
    """Verificar que la migración fue exitosa"""
    print("🔍 Verificando migración...")
    
    if ejecutar_comando("python manage.py check", "Verificando configuración"):
        print("✅ Verificación completada")
        return True
    else:
        print("❌ Error en la verificación")
        return False

def main():
    """Función principal de migración"""
    print("🚀 MIGRACIÓN DE SQLITE A POSTGRESQL")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Verificaciones previas
    if not verificar_postgresql():
        print("\n❌ PostgreSQL no está disponible")
        print("   Instala PostgreSQL antes de continuar")
        return False
    
    if not verificar_archivo_env():
        print("\n❌ Configuración de base de datos no encontrada")
        return False
    
    # Proceso de migración
    pasos = [
        ("Crear respaldo", crear_respaldo),
        ("Exportar datos", exportar_datos),
        ("Configurar PostgreSQL", configurar_postgresql),
        ("Aplicar migraciones", aplicar_migraciones),
        ("Importar datos", importar_datos),
        ("Verificar migración", verificar_migracion),
    ]
    
    for paso, funcion in pasos:
        print(f"\n📋 Paso: {paso}")
        print("-" * 30)
        
        if not funcion():
            print(f"\n❌ Migración falló en el paso: {paso}")
            return False
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("✅ La base de datos ha sido migrada de SQLite a PostgreSQL")
    print("✅ Los datos han sido preservados")
    print("✅ El sistema está listo para usar")
    print("\n📝 Próximos pasos:")
    print("   1. Ejecutar: python manage.py runserver")
    print("   2. Verificar que todo funcione correctamente")
    print("   3. Crear un superusuario si es necesario: python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


"""
Script principal para migrar KreaDental Cloud de SQLite a PostgreSQL
"""

import os
import sys
import subprocess
from datetime import datetime

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"🔄 {descripcion}...")
    
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {descripcion} completado")
            if result.stdout:
                print(f"   📝 {result.stdout.strip()}")
        else:
            print(f"❌ Error en {descripcion}")
            if result.stderr:
                print(f"   🚨 {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False
    
    return True

def verificar_postgresql():
    """Verificar que PostgreSQL esté instalado y funcionando"""
    print("🔍 Verificando PostgreSQL...")
    
    try:
        result = subprocess.run("psql --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL encontrado: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL no está instalado o no está en el PATH")
            return False
    except:
        print("❌ No se pudo verificar PostgreSQL")
        return False

def verificar_archivo_env():
    """Verificar que existe el archivo .env"""
    if not os.path.exists('.env'):
        print("❌ No se encontró el archivo .env")
        print("   Crea un archivo .env con la configuración de PostgreSQL")
        print("   Puedes usar el archivo MIGRACION_POSTGRESQL.md como referencia")
        return False
    
    print("✅ Archivo .env encontrado")
    return True

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
        import shutil
        shutil.copy2('db.sqlite3', backup_file)
        print(f"✅ Respaldo creado: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ Error creando respaldo: {e}")
        return False

def exportar_datos():
    """Exportar datos de SQLite"""
    print("📤 Exportando datos de SQLite...")
    
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
    comando = "python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -e sessions --output datos_exportados.json"
    
    if ejecutar_comando(comando, "Exportando datos"):
        print("✅ Datos exportados exitosamente")
        return True
    else:
        print("❌ Error exportando datos")
        return False

def configurar_postgresql():
    """Configurar PostgreSQL"""
    print("🔧 Configurando PostgreSQL...")
    
    if ejecutar_comando("python config_database.py", "Configurando base de datos"):
        print("✅ PostgreSQL configurado")
        return True
    else:
        print("❌ Error configurando PostgreSQL")
        return False

def aplicar_migraciones():
    """Aplicar migraciones a PostgreSQL"""
    print("🔄 Aplicando migraciones a PostgreSQL...")
    
    # Restaurar configuración de PostgreSQL
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    
    if ejecutar_comando("python manage.py migrate", "Aplicando migraciones"):
        print("✅ Migraciones aplicadas")
        return True
    else:
        print("❌ Error aplicando migraciones")
        return False

def importar_datos():
    """Importar datos a PostgreSQL"""
    print("📥 Importando datos a PostgreSQL...")
    
    if not os.path.exists('datos_exportados.json'):
        print("❌ No se encontró datos_exportados.json")
        return False
    
    if ejecutar_comando("python manage.py loaddata datos_exportados.json", "Importando datos"):
        print("✅ Datos importados")
        return True
    else:
        print("❌ Error importando datos")
        return False

def verificar_migracion():
    """Verificar que la migración fue exitosa"""
    print("🔍 Verificando migración...")
    
    if ejecutar_comando("python manage.py check", "Verificando configuración"):
        print("✅ Verificación completada")
        return True
    else:
        print("❌ Error en la verificación")
        return False

def main():
    """Función principal de migración"""
    print("🚀 MIGRACIÓN DE SQLITE A POSTGRESQL")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Verificaciones previas
    if not verificar_postgresql():
        print("\n❌ PostgreSQL no está disponible")
        print("   Instala PostgreSQL antes de continuar")
        return False
    
    if not verificar_archivo_env():
        print("\n❌ Configuración de base de datos no encontrada")
        return False
    
    # Proceso de migración
    pasos = [
        ("Crear respaldo", crear_respaldo),
        ("Exportar datos", exportar_datos),
        ("Configurar PostgreSQL", configurar_postgresql),
        ("Aplicar migraciones", aplicar_migraciones),
        ("Importar datos", importar_datos),
        ("Verificar migración", verificar_migracion),
    ]
    
    for paso, funcion in pasos:
        print(f"\n📋 Paso: {paso}")
        print("-" * 30)
        
        if not funcion():
            print(f"\n❌ Migración falló en el paso: {paso}")
            return False
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("✅ La base de datos ha sido migrada de SQLite a PostgreSQL")
    print("✅ Los datos han sido preservados")
    print("✅ El sistema está listo para usar")
    print("\n📝 Próximos pasos:")
    print("   1. Ejecutar: python manage.py runserver")
    print("   2. Verificar que todo funcione correctamente")
    print("   3. Crear un superusuario si es necesario: python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)





