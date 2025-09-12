#!/usr/bin/env python
"""
Script para crear la estructura de PostgreSQL usando psycopg2
Basado en el enfoque del usuario para manejar encoding correctamente
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json

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

def crear_tablas_desde_sqlite():
    """Crear las tablas en PostgreSQL basándose en la estructura de SQLite"""
    
    # Primero, vamos a obtener la estructura desde SQLite
    import sqlite3
    
    try:
        # Conectar a SQLite
        sqlite_conn = sqlite3.connect('db.sqlite3')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obtener todas las tablas
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [row[0] for row in sqlite_cursor.fetchall()]
        
        print(f"📋 Tablas encontradas en SQLite: {len(tablas)}")
        
        # Crear diccionario de estructuras
        estructuras = {}
        
        for tabla in tablas:
            if tabla.startswith('django_') or tabla == 'sqlite_sequence':
                continue
                
            # Obtener estructura de la tabla
            sqlite_cursor.execute(f"PRAGMA table_info({tabla})")
            columnas = sqlite_cursor.fetchall()
            
            estructuras[tabla] = columnas
            print(f"   - {tabla}: {len(columnas)} columnas")
        
        sqlite_conn.close()
        return estructuras
        
    except Exception as e:
        print(f"❌ Error obteniendo estructura de SQLite: {e}")
        return {}

def crear_tabla_en_postgresql(conn, nombre_tabla, columnas):
    """Crear una tabla en PostgreSQL"""
    try:
        cur = conn.cursor()
        
        # Construir la consulta CREATE TABLE
        columnas_sql = []
        
        for col in columnas:
            cid, nombre, tipo, not_null, default, pk = col
            
            # Mapear tipos de SQLite a PostgreSQL
            if tipo.upper() == 'INTEGER':
                tipo_pg = 'SERIAL PRIMARY KEY' if pk else 'INTEGER'
            elif tipo.upper() == 'TEXT':
                tipo_pg = 'TEXT'
            elif tipo.upper() == 'REAL':
                tipo_pg = 'REAL'
            elif tipo.upper() == 'BLOB':
                tipo_pg = 'BYTEA'
            elif 'VARCHAR' in tipo.upper():
                tipo_pg = tipo
            else:
                tipo_pg = 'TEXT'
            
            # Agregar restricciones
            if not_null and not pk:
                tipo_pg += ' NOT NULL'
            
            columnas_sql.append(f'"{nombre}" {tipo_pg}')
        
        # Crear la tabla
        query = f'CREATE TABLE IF NOT EXISTS "{nombre_tabla}" (\n    {",\n    ".join(columnas_sql)}\n);'
        
        print(f"🔨 Creando tabla: {nombre_tabla}")
        cur.execute(query)
        conn.commit()
        
        print(f"✅ Tabla {nombre_tabla} creada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando tabla {nombre_tabla}: {e}")
        conn.rollback()
        return False

def migrar_datos_tabla(conn, nombre_tabla, columnas):
    """Migrar datos de una tabla específica desde SQLite a PostgreSQL"""
    try:
        import sqlite3
        
        # Conectar a SQLite
        sqlite_conn = sqlite3.connect('db.sqlite3')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obtener datos de SQLite
        sqlite_cursor.execute(f'SELECT * FROM "{nombre_tabla}"')
        datos = sqlite_cursor.fetchall()
        
        if not datos:
            print(f"   ⚠️  No hay datos en {nombre_tabla}")
            sqlite_conn.close()
            return True
        
        # Preparar datos para PostgreSQL
        cur = conn.cursor()
        
        # Obtener nombres de columnas
        nombres_columnas = [col[1] for col in columnas]
        placeholders = ', '.join(['%s'] * len(nombres_columnas))
        
        # Insertar datos
        columnas_quoted = [f'"{col}"' for col in nombres_columnas]
        query = f'INSERT INTO "{nombre_tabla}" ({", ".join(columnas_quoted)}) VALUES ({placeholders})'
        
        registros_migrados = 0
        for fila in datos:
            try:
                # Convertir datos para PostgreSQL
                fila_convertida = []
                for i, valor in enumerate(fila):
                    if valor is None:
                        fila_convertida.append(None)
                    elif isinstance(valor, str):
                        # Manejar encoding correctamente
                        fila_convertida.append(valor.encode('utf-8', errors='ignore').decode('utf-8'))
                    else:
                        fila_convertida.append(valor)
                
                cur.execute(query, fila_convertida)
                registros_migrados += 1
                
            except Exception as e:
                print(f"   ⚠️  Error migrando fila: {e}")
                continue
        
        conn.commit()
        sqlite_conn.close()
        
        print(f"   ✅ {registros_migrados} registros migrados a {nombre_tabla}")
        return True
        
    except Exception as e:
        print(f"❌ Error migrando datos de {nombre_tabla}: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Creando estructura de PostgreSQL desde SQLite")
    print("=" * 60)
    
    # 1. Conectar a PostgreSQL
    conn = conectar_postgresql()
    if not conn:
        return False
    
    try:
        # 2. Obtener estructura de SQLite
        print("\n📊 Obteniendo estructura de SQLite...")
        estructuras = crear_tablas_desde_sqlite()
        
        if not estructuras:
            print("❌ No se pudo obtener la estructura de SQLite")
            return False
        
        # 3. Crear tablas en PostgreSQL
        print("\n🔨 Creando tablas en PostgreSQL...")
        tablas_creadas = 0
        
        for nombre_tabla, columnas in estructuras.items():
            if crear_tabla_en_postgresql(conn, nombre_tabla, columnas):
                tablas_creadas += 1
        
        print(f"\n✅ {tablas_creadas} tablas creadas en PostgreSQL")
        
        # 4. Migrar datos
        print("\n📦 Migrando datos...")
        tablas_migradas = 0
        
        for nombre_tabla, columnas in estructuras.items():
            if migrar_datos_tabla(conn, nombre_tabla, columnas):
                tablas_migradas += 1
        
        print(f"\n✅ {tablas_migradas} tablas migradas con datos")
        
        # 5. Verificar migración
        print("\n🔍 Verificando migración...")
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tablas_postgresql = [row[0] for row in cur.fetchall()]
        print(f"📊 Tablas en PostgreSQL: {len(tablas_postgresql)}")
        
        total_registros = 0
        for tabla in tablas_postgresql:
            try:
                cur.execute(f'SELECT COUNT(*) FROM "{tabla}"')
                count = cur.fetchone()[0]
                total_registros += count
                print(f"   {tabla}: {count} registros")
            except Exception as e:
                print(f"   {tabla}: Error - {e}")
        
        print(f"\n🎉 ¡Migración completada!")
        print(f"📈 Total de registros migrados: {total_registros}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

Script para crear la estructura de PostgreSQL usando psycopg2
Basado en el enfoque del usuario para manejar encoding correctamente
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json

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

def crear_tablas_desde_sqlite():
    """Crear las tablas en PostgreSQL basándose en la estructura de SQLite"""
    
    # Primero, vamos a obtener la estructura desde SQLite
    import sqlite3
    
    try:
        # Conectar a SQLite
        sqlite_conn = sqlite3.connect('db.sqlite3')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obtener todas las tablas
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [row[0] for row in sqlite_cursor.fetchall()]
        
        print(f"📋 Tablas encontradas en SQLite: {len(tablas)}")
        
        # Crear diccionario de estructuras
        estructuras = {}
        
        for tabla in tablas:
            if tabla.startswith('django_') or tabla == 'sqlite_sequence':
                continue
                
            # Obtener estructura de la tabla
            sqlite_cursor.execute(f"PRAGMA table_info({tabla})")
            columnas = sqlite_cursor.fetchall()
            
            estructuras[tabla] = columnas
            print(f"   - {tabla}: {len(columnas)} columnas")
        
        sqlite_conn.close()
        return estructuras
        
    except Exception as e:
        print(f"❌ Error obteniendo estructura de SQLite: {e}")
        return {}

def crear_tabla_en_postgresql(conn, nombre_tabla, columnas):
    """Crear una tabla en PostgreSQL"""
    try:
        cur = conn.cursor()
        
        # Construir la consulta CREATE TABLE
        columnas_sql = []
        
        for col in columnas:
            cid, nombre, tipo, not_null, default, pk = col
            
            # Mapear tipos de SQLite a PostgreSQL
            if tipo.upper() == 'INTEGER':
                tipo_pg = 'SERIAL PRIMARY KEY' if pk else 'INTEGER'
            elif tipo.upper() == 'TEXT':
                tipo_pg = 'TEXT'
            elif tipo.upper() == 'REAL':
                tipo_pg = 'REAL'
            elif tipo.upper() == 'BLOB':
                tipo_pg = 'BYTEA'
            elif 'VARCHAR' in tipo.upper():
                tipo_pg = tipo
            else:
                tipo_pg = 'TEXT'
            
            # Agregar restricciones
            if not_null and not pk:
                tipo_pg += ' NOT NULL'
            
            columnas_sql.append(f'"{nombre}" {tipo_pg}')
        
        # Crear la tabla
        query = f'CREATE TABLE IF NOT EXISTS "{nombre_tabla}" (\n    {",\n    ".join(columnas_sql)}\n);'
        
        print(f"🔨 Creando tabla: {nombre_tabla}")
        cur.execute(query)
        conn.commit()
        
        print(f"✅ Tabla {nombre_tabla} creada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando tabla {nombre_tabla}: {e}")
        conn.rollback()
        return False

def migrar_datos_tabla(conn, nombre_tabla, columnas):
    """Migrar datos de una tabla específica desde SQLite a PostgreSQL"""
    try:
        import sqlite3
        
        # Conectar a SQLite
        sqlite_conn = sqlite3.connect('db.sqlite3')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obtener datos de SQLite
        sqlite_cursor.execute(f'SELECT * FROM "{nombre_tabla}"')
        datos = sqlite_cursor.fetchall()
        
        if not datos:
            print(f"   ⚠️  No hay datos en {nombre_tabla}")
            sqlite_conn.close()
            return True
        
        # Preparar datos para PostgreSQL
        cur = conn.cursor()
        
        # Obtener nombres de columnas
        nombres_columnas = [col[1] for col in columnas]
        placeholders = ', '.join(['%s'] * len(nombres_columnas))
        
        # Insertar datos
        columnas_quoted = [f'"{col}"' for col in nombres_columnas]
        query = f'INSERT INTO "{nombre_tabla}" ({", ".join(columnas_quoted)}) VALUES ({placeholders})'
        
        registros_migrados = 0
        for fila in datos:
            try:
                # Convertir datos para PostgreSQL
                fila_convertida = []
                for i, valor in enumerate(fila):
                    if valor is None:
                        fila_convertida.append(None)
                    elif isinstance(valor, str):
                        # Manejar encoding correctamente
                        fila_convertida.append(valor.encode('utf-8', errors='ignore').decode('utf-8'))
                    else:
                        fila_convertida.append(valor)
                
                cur.execute(query, fila_convertida)
                registros_migrados += 1
                
            except Exception as e:
                print(f"   ⚠️  Error migrando fila: {e}")
                continue
        
        conn.commit()
        sqlite_conn.close()
        
        print(f"   ✅ {registros_migrados} registros migrados a {nombre_tabla}")
        return True
        
    except Exception as e:
        print(f"❌ Error migrando datos de {nombre_tabla}: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Creando estructura de PostgreSQL desde SQLite")
    print("=" * 60)
    
    # 1. Conectar a PostgreSQL
    conn = conectar_postgresql()
    if not conn:
        return False
    
    try:
        # 2. Obtener estructura de SQLite
        print("\n📊 Obteniendo estructura de SQLite...")
        estructuras = crear_tablas_desde_sqlite()
        
        if not estructuras:
            print("❌ No se pudo obtener la estructura de SQLite")
            return False
        
        # 3. Crear tablas en PostgreSQL
        print("\n🔨 Creando tablas en PostgreSQL...")
        tablas_creadas = 0
        
        for nombre_tabla, columnas in estructuras.items():
            if crear_tabla_en_postgresql(conn, nombre_tabla, columnas):
                tablas_creadas += 1
        
        print(f"\n✅ {tablas_creadas} tablas creadas en PostgreSQL")
        
        # 4. Migrar datos
        print("\n📦 Migrando datos...")
        tablas_migradas = 0
        
        for nombre_tabla, columnas in estructuras.items():
            if migrar_datos_tabla(conn, nombre_tabla, columnas):
                tablas_migradas += 1
        
        print(f"\n✅ {tablas_migradas} tablas migradas con datos")
        
        # 5. Verificar migración
        print("\n🔍 Verificando migración...")
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tablas_postgresql = [row[0] for row in cur.fetchall()]
        print(f"📊 Tablas en PostgreSQL: {len(tablas_postgresql)}")
        
        total_registros = 0
        for tabla in tablas_postgresql:
            try:
                cur.execute(f'SELECT COUNT(*) FROM "{tabla}"')
                count = cur.fetchone()[0]
                total_registros += count
                print(f"   {tabla}: {count} registros")
            except Exception as e:
                print(f"   {tabla}: Error - {e}")
        
        print(f"\n🎉 ¡Migración completada!")
        print(f"📈 Total de registros migrados: {total_registros}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
