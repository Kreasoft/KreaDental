#!/usr/bin/env python
"""
Script para configurar la base de datos PostgreSQL para KreaDental Cloud
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def crear_base_datos():
    """Crear la base de datos PostgreSQL si no existe"""
    
    # Configuración de conexión (sin especificar base de datos)
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
    }
    
    db_name = os.getenv('DB_NAME', 'kreadental_cloud')
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            # Crear la base de datos
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Base de datos '{db_name}' creada exitosamente")
        else:
            print(f"ℹ️  La base de datos '{db_name}' ya existe")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error al crear la base de datos: {e}")
        return False
    
    return True

def verificar_conexion():
    """Verificar la conexión a la base de datos"""
    
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'kreadental_cloud'),
    }
    
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Conexión exitosa a PostgreSQL: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Configurando base de datos PostgreSQL para KreaDental Cloud")
    print("=" * 60)
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    # Verificar variables de entorno
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Faltan las siguientes variables de entorno:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPor favor, configura las variables en un archivo .env")
        exit(1)
    
    # Crear base de datos
    if crear_base_datos():
        # Verificar conexión
        if verificar_conexion():
            print("\n🎉 Configuración completada exitosamente!")
            print("Ahora puedes ejecutar: python manage.py migrate")
        else:
            print("\n❌ Error en la verificación de conexión")
    else:
        print("\n❌ Error al crear la base de datos")


"""
Script para configurar la base de datos PostgreSQL para KreaDental Cloud
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def crear_base_datos():
    """Crear la base de datos PostgreSQL si no existe"""
    
    # Configuración de conexión (sin especificar base de datos)
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
    }
    
    db_name = os.getenv('DB_NAME', 'kreadental_cloud')
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            # Crear la base de datos
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Base de datos '{db_name}' creada exitosamente")
        else:
            print(f"ℹ️  La base de datos '{db_name}' ya existe")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error al crear la base de datos: {e}")
        return False
    
    return True

def verificar_conexion():
    """Verificar la conexión a la base de datos"""
    
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'kreadental_cloud'),
    }
    
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Conexión exitosa a PostgreSQL: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Configurando base de datos PostgreSQL para KreaDental Cloud")
    print("=" * 60)
    
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    # Verificar variables de entorno
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Faltan las siguientes variables de entorno:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPor favor, configura las variables en un archivo .env")
        exit(1)
    
    # Crear base de datos
    if crear_base_datos():
        # Verificar conexión
        if verificar_conexion():
            print("\n🎉 Configuración completada exitosamente!")
            print("Ahora puedes ejecutar: python manage.py migrate")
        else:
            print("\n❌ Error en la verificación de conexión")
    else:
        print("\n❌ Error al crear la base de datos")





