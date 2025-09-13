#!/usr/bin/env python
"""
Script para solucionar el problema UTF-8 con configuración específica
"""
import os
import sys
import subprocess
import psycopg2
from pathlib import Path

def probar_conexion_con_configuracion_especifica():
    """Prueba la conexión con configuración específica para evitar UTF-8"""
    print("🔍 Probando conexión con configuración específica...")
    
    try:
        # Configuración específica para evitar problemas UTF-8
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='postgres',
            port='5432',
            options='-c client_encoding=UTF8'
        )
        print("✅ Conexión exitosa con configuración específica")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error con configuración específica: {e}")
        return False

def crear_base_datos_con_configuracion_especifica():
    """Crea la base de datos con configuración específica"""
    print("\n🗄️ Creando base de datos con configuración específica...")
    
    try:
        # Conectar a postgres
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='postgres',
            port='5432',
            options='-c client_encoding=UTF8'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Eliminar base de datos si existe
        cursor.execute("DROP DATABASE IF EXISTS kreadental_final;")
        print("✅ Base de datos existente eliminada")
        
        # Crear nueva base de datos
        cursor.execute("CREATE DATABASE kreadental_final WITH ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;")
        print("✅ Base de datos creada con configuración específica")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def probar_django_con_configuracion_especifica():
    """Prueba Django con configuración específica"""
    print("\n🔄 Probando Django con configuración específica...")
    
    # Crear configuración específica
    config_especifica = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kreadental_final',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}"""
    
    try:
        # Leer archivo settings
        settings_file = "config/settings.py"
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar configuración
        old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
        
        content = content.replace(old_config, config_especifica)
        
        # Escribir archivo
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuración específica aplicada")
        
        # Probar Django
        result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ Django funciona con configuración específica")
            return True
        else:
            print(f"❌ Django falló: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando Django: {e}")
        return False

def aplicar_migraciones_con_configuracion_especifica():
    """Aplica migraciones con configuración específica"""
    print("\n🔄 Aplicando migraciones con configuración específica...")
    
    try:
        result = subprocess.run(['python', 'manage.py', 'migrate'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ Migraciones aplicadas exitosamente")
            return True
        else:
            print(f"❌ Error aplicando migraciones: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error aplicando migraciones: {e}")
        return False

def importar_datos_con_configuracion_especifica():
    """Importa datos con configuración específica"""
    print("\n📥 Importando datos con configuración específica...")
    
    try:
        result = subprocess.run(['python', 'manage.py', 'loaddata', 'datos_exportados.json'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ Datos importados exitosamente")
            return True
        else:
            print(f"❌ Error importando datos: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error importando datos: {e}")
        return False

def verificar_migracion_completa():
    """Verifica que la migración completa fue exitosa"""
    print("\n🔍 Verificando migración completa...")
    
    try:
        # Verificar Django
        result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"❌ Django check falló: {result.stderr}")
            return False
        
        print("✅ Django check exitoso")
        
        # Verificar tablas en PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            database='kreadental_final',
            user='postgres',
            password='postgres',
            port='5432',
            options='-c client_encoding=UTF8'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = cursor.fetchall()
        print(f"✅ Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando solución UTF-8 con configuración específica...")
    
    # Paso 1: Probar conexión con configuración específica
    if not probar_conexion_con_configuracion_especifica():
        print("❌ No se puede conectar con configuración específica")
        return
    
    # Paso 2: Crear base de datos con configuración específica
    if not crear_base_datos_con_configuracion_especifica():
        print("❌ No se pudo crear la base de datos con configuración específica")
        return
    
    # Paso 3: Probar Django con configuración específica
    if not probar_django_con_configuracion_especifica():
        print("❌ Django no funciona con configuración específica")
        return
    
    # Paso 4: Aplicar migraciones
    if not aplicar_migraciones_con_configuracion_especifica():
        print("❌ No se pudieron aplicar las migraciones")
        return
    
    # Paso 5: Importar datos
    if not importar_datos_con_configuracion_especifica():
        print("❌ No se pudieron importar los datos")
        return
    
    # Paso 6: Verificar migración completa
    if not verificar_migracion_completa():
        print("❌ La migración no se completó correctamente")
        return
    
    print("\n🎉 ¡Migración completada exitosamente con configuración específica!")
    print("📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Verifica que la aplicación funciona en el navegador")

if __name__ == "__main__":
    main()

"""
Script para solucionar el problema UTF-8 con configuración específica
"""
import os
import sys
import subprocess
import psycopg2
from pathlib import Path

def probar_conexion_con_configuracion_especifica():
    """Prueba la conexión con configuración específica para evitar UTF-8"""
    print("🔍 Probando conexión con configuración específica...")
    
    try:
        # Configuración específica para evitar problemas UTF-8
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='postgres',
            port='5432',
            options='-c client_encoding=UTF8'
        )
        print("✅ Conexión exitosa con configuración específica")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error con configuración específica: {e}")
        return False

def crear_base_datos_con_configuracion_especifica():
    """Crea la base de datos con configuración específica"""
    print("\n🗄️ Creando base de datos con configuración específica...")
    
    try:
        # Conectar a postgres
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='postgres',
            port='5432',
            options='-c client_encoding=UTF8'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Eliminar base de datos si existe
        cursor.execute("DROP DATABASE IF EXISTS kreadental_final;")
        print("✅ Base de datos existente eliminada")
        
        # Crear nueva base de datos
        cursor.execute("CREATE DATABASE kreadental_final WITH ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;")
        print("✅ Base de datos creada con configuración específica")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def probar_django_con_configuracion_especifica():
    """Prueba Django con configuración específica"""
    print("\n🔄 Probando Django con configuración específica...")
    
    # Crear configuración específica
    config_especifica = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kreadental_final',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}"""
    
    try:
        # Leer archivo settings
        settings_file = "config/settings.py"
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar configuración
        old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
        
        content = content.replace(old_config, config_especifica)
        
        # Escribir archivo
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuración específica aplicada")
        
        # Probar Django
        result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ Django funciona con configuración específica")
            return True
        else:
            print(f"❌ Django falló: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando Django: {e}")
        return False

def aplicar_migraciones_con_configuracion_especifica():
    """Aplica migraciones con configuración específica"""
    print("\n🔄 Aplicando migraciones con configuración específica...")
    
    try:
        result = subprocess.run(['python', 'manage.py', 'migrate'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ Migraciones aplicadas exitosamente")
            return True
        else:
            print(f"❌ Error aplicando migraciones: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error aplicando migraciones: {e}")
        return False

def importar_datos_con_configuracion_especifica():
    """Importa datos con configuración específica"""
    print("\n📥 Importando datos con configuración específica...")
    
    try:
        result = subprocess.run(['python', 'manage.py', 'loaddata', 'datos_exportados.json'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ Datos importados exitosamente")
            return True
        else:
            print(f"❌ Error importando datos: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error importando datos: {e}")
        return False

def verificar_migracion_completa():
    """Verifica que la migración completa fue exitosa"""
    print("\n🔍 Verificando migración completa...")
    
    try:
        # Verificar Django
        result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"❌ Django check falló: {result.stderr}")
            return False
        
        print("✅ Django check exitoso")
        
        # Verificar tablas en PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            database='kreadental_final',
            user='postgres',
            password='postgres',
            port='5432',
            options='-c client_encoding=UTF8'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = cursor.fetchall()
        print(f"✅ Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando solución UTF-8 con configuración específica...")
    
    # Paso 1: Probar conexión con configuración específica
    if not probar_conexion_con_configuracion_especifica():
        print("❌ No se puede conectar con configuración específica")
        return
    
    # Paso 2: Crear base de datos con configuración específica
    if not crear_base_datos_con_configuracion_especifica():
        print("❌ No se pudo crear la base de datos con configuración específica")
        return
    
    # Paso 3: Probar Django con configuración específica
    if not probar_django_con_configuracion_especifica():
        print("❌ Django no funciona con configuración específica")
        return
    
    # Paso 4: Aplicar migraciones
    if not aplicar_migraciones_con_configuracion_especifica():
        print("❌ No se pudieron aplicar las migraciones")
        return
    
    # Paso 5: Importar datos
    if not importar_datos_con_configuracion_especifica():
        print("❌ No se pudieron importar los datos")
        return
    
    # Paso 6: Verificar migración completa
    if not verificar_migracion_completa():
        print("❌ La migración no se completó correctamente")
        return
    
    print("\n🎉 ¡Migración completada exitosamente con configuración específica!")
    print("📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Verifica que la aplicación funciona en el navegador")

if __name__ == "__main__":
    main()






