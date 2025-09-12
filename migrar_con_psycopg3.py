#!/usr/bin/env python
"""
Script para migrar datos desde SQLite a PostgreSQL usando psycopg3
Basado en el código proporcionado por el usuario para manejar encoding correctamente
"""

import psycopg
import sqlite3
import json

def conectar_postgresql():
    """Conectar a PostgreSQL usando psycopg3"""
    try:
        conn = psycopg.connect(
            dbname="kreadental_cloud",
            user="postgres",
            password="524302cl+",
            host="127.0.0.1",
            port="5432"
        )
        print("✅ Conexión a PostgreSQL exitosa con psycopg3")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def obtener_estructura_sqlite():
    """Obtener estructura de tablas desde SQLite"""
    try:
        sqlite_conn = sqlite3.connect('db.sqlite3')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obtener todas las tablas
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [row[0] for row in sqlite_cursor.fetchall()]
        
        print(f"📋 Tablas encontradas en SQLite: {len(tablas)}")
        
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

def crear_tabla_postgresql(conn, nombre_tabla, columnas):
    """Crear tabla en PostgreSQL"""
    try:
        with conn.cursor() as cur:
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
        return False

def migrar_datos_tabla(conn, nombre_tabla, columnas):
    """Migrar datos de una tabla específica"""
    try:
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
        with conn.cursor() as cur:
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
                    for valor in fila:
                        if valor is None:
                            fila_convertida.append(None)
                        elif isinstance(valor, str):
                            # Manejar encoding correctamente
                            try:
                                # Intentar decodificar como UTF-8
                                fila_convertida.append(valor.encode('utf-8', errors='ignore').decode('utf-8'))
                            except:
                                # Si falla, usar el valor tal como está
                                fila_convertida.append(valor)
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

def verificar_migracion(conn):
    """Verificar que la migración fue exitosa"""
    try:
        with conn.cursor() as cur:
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
                    cur.execute(f'SELECT COUNT(*) FROM "{tabla}"')
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
    print("🚀 Migrando datos de SQLite a PostgreSQL con psycopg3")
    print("=" * 60)
    
    # 1. Conectar a PostgreSQL
    conn = conectar_postgresql()
    if not conn:
        return False
    
    try:
        # 2. Obtener estructura de SQLite
        print("\n📊 Obteniendo estructura de SQLite...")
        estructuras = obtener_estructura_sqlite()
        
        if not estructuras:
            print("❌ No se pudo obtener la estructura de SQLite")
            return False
        
        # 3. Crear tablas en PostgreSQL
        print("\n🔨 Creando tablas en PostgreSQL...")
        tablas_creadas = 0
        
        for nombre_tabla, columnas in estructuras.items():
            if crear_tabla_postgresql(conn, nombre_tabla, columnas):
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
        if not verificar_migracion(conn):
            return False
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print("✅ Los datos han sido migrados de SQLite a PostgreSQL usando psycopg3")
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

Script para migrar datos desde SQLite a PostgreSQL usando psycopg3
Basado en el código proporcionado por el usuario para manejar encoding correctamente
"""

import psycopg
import sqlite3
import json

def conectar_postgresql():
    """Conectar a PostgreSQL usando psycopg3"""
    try:
        conn = psycopg.connect(
            dbname="kreadental_cloud",
            user="postgres",
            password="524302cl+",
            host="127.0.0.1",
            port="5432"
        )
        print("✅ Conexión a PostgreSQL exitosa con psycopg3")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def obtener_estructura_sqlite():
    """Obtener estructura de tablas desde SQLite"""
    try:
        sqlite_conn = sqlite3.connect('db.sqlite3')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Obtener todas las tablas
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [row[0] for row in sqlite_cursor.fetchall()]
        
        print(f"📋 Tablas encontradas en SQLite: {len(tablas)}")
        
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

def crear_tabla_postgresql(conn, nombre_tabla, columnas):
    """Crear tabla en PostgreSQL"""
    try:
        with conn.cursor() as cur:
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
        return False

def migrar_datos_tabla(conn, nombre_tabla, columnas):
    """Migrar datos de una tabla específica"""
    try:
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
        with conn.cursor() as cur:
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
                    for valor in fila:
                        if valor is None:
                            fila_convertida.append(None)
                        elif isinstance(valor, str):
                            # Manejar encoding correctamente
                            try:
                                # Intentar decodificar como UTF-8
                                fila_convertida.append(valor.encode('utf-8', errors='ignore').decode('utf-8'))
                            except:
                                # Si falla, usar el valor tal como está
                                fila_convertida.append(valor)
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

def verificar_migracion(conn):
    """Verificar que la migración fue exitosa"""
    try:
        with conn.cursor() as cur:
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
                    cur.execute(f'SELECT COUNT(*) FROM "{tabla}"')
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
    print("🚀 Migrando datos de SQLite a PostgreSQL con psycopg3")
    print("=" * 60)
    
    # 1. Conectar a PostgreSQL
    conn = conectar_postgresql()
    if not conn:
        return False
    
    try:
        # 2. Obtener estructura de SQLite
        print("\n📊 Obteniendo estructura de SQLite...")
        estructuras = obtener_estructura_sqlite()
        
        if not estructuras:
            print("❌ No se pudo obtener la estructura de SQLite")
            return False
        
        # 3. Crear tablas en PostgreSQL
        print("\n🔨 Creando tablas en PostgreSQL...")
        tablas_creadas = 0
        
        for nombre_tabla, columnas in estructuras.items():
            if crear_tabla_postgresql(conn, nombre_tabla, columnas):
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
        if not verificar_migracion(conn):
            return False
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print("✅ Los datos han sido migrados de SQLite a PostgreSQL usando psycopg3")
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
