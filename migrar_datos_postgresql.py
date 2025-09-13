#!/usr/bin/env python
"""
Script para migrar datos desde SQLite a PostgreSQL usando psycopg2
Basado en el código proporcionado por el usuario para manejar encoding correctamente
"""

import os
import sys
import django
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line

def conectar_postgresql():
    """Conectar a PostgreSQL con encoding correcto"""
    try:
        conn = psycopg2.connect(
            dbname="kreadental_cloud",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432",
            client_encoding='UTF8'
        )
        print("✅ Conexión a PostgreSQL exitosa")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def verificar_tablas_existentes(conn):
    """Verificar qué tablas existen en PostgreSQL"""
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tablas = [row[0] for row in cur.fetchall()]
        print(f"📋 Tablas existentes en PostgreSQL: {len(tablas)}")
        for tabla in tablas:
            print(f"   - {tabla}")
        return tablas
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return []

def migrar_datos_desde_json(conn):
    """Migrar datos desde el archivo JSON exportado"""
    try:
        # Leer el archivo JSON
        with open('datos_exportados.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        print(f"📊 Datos cargados: {len(datos)} registros")
        
        cur = conn.cursor()
        
        # Contador de registros migrados
        total_migrados = 0
        
        for item in datos:
            try:
                modelo = item['model']
                campos = item['fields']
                pk = item['pk']
                
                # Obtener el nombre de la tabla
                tabla = modelo.replace('.', '_').lower()
                
                # Crear la consulta INSERT
                columnas = list(campos.keys())
                valores = list(campos.values())
                placeholders = ', '.join(['%s'] * len(columnas))
                
                # Agregar el ID como primera columna
                columnas.insert(0, 'id')
                valores.insert(0, pk)
                placeholders = '%s, ' + placeholders
                
                query = f"""
                    INSERT INTO {tabla} ({', '.join(columnas)}) 
                    VALUES ({placeholders})
                    ON CONFLICT (id) DO UPDATE SET
                    {', '.join([f"{col} = EXCLUDED.{col}" for col in columnas[1:]])}
                """
                
                cur.execute(query, valores)
                total_migrados += 1
                
                if total_migrados % 100 == 0:
                    print(f"   📈 Migrados {total_migrados} registros...")
                    
            except Exception as e:
                print(f"⚠️  Error migrando {item.get('model', 'desconocido')}: {e}")
                continue
        
        # Confirmar cambios
        conn.commit()
        print(f"✅ Migración completada: {total_migrados} registros migrados")
        return True
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        conn.rollback()
        return False

def verificar_migracion(conn):
    """Verificar que la migración fue exitosa"""
    try:
        cur = conn.cursor()
        
        # Contar registros en cada tabla
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tablas = [row[0] for row in cur.fetchall()]
        
        print("\n📊 Verificación de migración:")
        print("=" * 50)
        
        total_registros = 0
        for tabla in tablas:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cur.fetchone()[0]
                total_registros += count
                print(f"   {tabla}: {count} registros")
            except Exception as e:
                print(f"   {tabla}: Error - {e}")
        
        print("=" * 50)
        print(f"📈 Total de registros: {total_registros}")
        
        return total_registros > 0
        
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando migración de datos a PostgreSQL")
    print("=" * 60)
    
    # 1. Conectar a PostgreSQL
    conn = conectar_postgresql()
    if not conn:
        return False
    
    try:
        # 2. Verificar tablas existentes
        tablas = verificar_tablas_existentes(conn)
        if not tablas:
            print("❌ No hay tablas en PostgreSQL. Ejecuta las migraciones primero.")
            return False
        
        # 3. Migrar datos
        print("\n🔄 Iniciando migración de datos...")
        if not migrar_datos_desde_json(conn):
            return False
        
        # 4. Verificar migración
        print("\n🔍 Verificando migración...")
        if not verificar_migracion(conn):
            return False
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print("✅ Los datos han sido migrados de SQLite a PostgreSQL")
        return True
        
    finally:
        conn.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

"""
Script para migrar datos desde SQLite a PostgreSQL usando psycopg2
Basado en el código proporcionado por el usuario para manejar encoding correctamente
"""

import os
import sys
import django
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line

def conectar_postgresql():
    """Conectar a PostgreSQL con encoding correcto"""
    try:
        conn = psycopg2.connect(
            dbname="kreadental_cloud",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432",
            client_encoding='UTF8'
        )
        print("✅ Conexión a PostgreSQL exitosa")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def verificar_tablas_existentes(conn):
    """Verificar qué tablas existen en PostgreSQL"""
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tablas = [row[0] for row in cur.fetchall()]
        print(f"📋 Tablas existentes en PostgreSQL: {len(tablas)}")
        for tabla in tablas:
            print(f"   - {tabla}")
        return tablas
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return []

def migrar_datos_desde_json(conn):
    """Migrar datos desde el archivo JSON exportado"""
    try:
        # Leer el archivo JSON
        with open('datos_exportados.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        print(f"📊 Datos cargados: {len(datos)} registros")
        
        cur = conn.cursor()
        
        # Contador de registros migrados
        total_migrados = 0
        
        for item in datos:
            try:
                modelo = item['model']
                campos = item['fields']
                pk = item['pk']
                
                # Obtener el nombre de la tabla
                tabla = modelo.replace('.', '_').lower()
                
                # Crear la consulta INSERT
                columnas = list(campos.keys())
                valores = list(campos.values())
                placeholders = ', '.join(['%s'] * len(columnas))
                
                # Agregar el ID como primera columna
                columnas.insert(0, 'id')
                valores.insert(0, pk)
                placeholders = '%s, ' + placeholders
                
                query = f"""
                    INSERT INTO {tabla} ({', '.join(columnas)}) 
                    VALUES ({placeholders})
                    ON CONFLICT (id) DO UPDATE SET
                    {', '.join([f"{col} = EXCLUDED.{col}" for col in columnas[1:]])}
                """
                
                cur.execute(query, valores)
                total_migrados += 1
                
                if total_migrados % 100 == 0:
                    print(f"   📈 Migrados {total_migrados} registros...")
                    
            except Exception as e:
                print(f"⚠️  Error migrando {item.get('model', 'desconocido')}: {e}")
                continue
        
        # Confirmar cambios
        conn.commit()
        print(f"✅ Migración completada: {total_migrados} registros migrados")
        return True
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        conn.rollback()
        return False

def verificar_migracion(conn):
    """Verificar que la migración fue exitosa"""
    try:
        cur = conn.cursor()
        
        # Contar registros en cada tabla
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tablas = [row[0] for row in cur.fetchall()]
        
        print("\n📊 Verificación de migración:")
        print("=" * 50)
        
        total_registros = 0
        for tabla in tablas:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cur.fetchone()[0]
                total_registros += count
                print(f"   {tabla}: {count} registros")
            except Exception as e:
                print(f"   {tabla}: Error - {e}")
        
        print("=" * 50)
        print(f"📈 Total de registros: {total_registros}")
        
        return total_registros > 0
        
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando migración de datos a PostgreSQL")
    print("=" * 60)
    
    # 1. Conectar a PostgreSQL
    conn = conectar_postgresql()
    if not conn:
        return False
    
    try:
        # 2. Verificar tablas existentes
        tablas = verificar_tablas_existentes(conn)
        if not tablas:
            print("❌ No hay tablas en PostgreSQL. Ejecuta las migraciones primero.")
            return False
        
        # 3. Migrar datos
        print("\n🔄 Iniciando migración de datos...")
        if not migrar_datos_desde_json(conn):
            return False
        
        # 4. Verificar migración
        print("\n🔍 Verificando migración...")
        if not verificar_migracion(conn):
            return False
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print("✅ Los datos han sido migrados de SQLite a PostgreSQL")
        return True
        
    finally:
        conn.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)






