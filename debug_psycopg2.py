#!/usr/bin/env python
"""
Script para debuggear específicamente psycopg2
"""
import os
import sys
import subprocess

def verificar_version_psycopg2():
    """Verifica la versión de psycopg2"""
    print("🔍 Verificando versión de psycopg2...")
    try:
        import psycopg2
        print(f"✅ psycopg2 versión: {psycopg2.__version__}")
        return True
    except Exception as e:
        print(f"❌ Error importando psycopg2: {e}")
        return False

def probar_conexion_con_diferentes_encodings():
    """Prueba la conexión con diferentes encodings"""
    print("\n🔍 Probando conexión con diferentes encodings...")
    
    try:
        import psycopg2
        
        # Probar con diferentes configuraciones de encoding
        configuraciones = [
            {'host': 'localhost', 'database': 'postgres', 'user': 'postgres', 'password': 'postgres', 'port': '5432'},
            {'host': '127.0.0.1', 'database': 'postgres', 'user': 'postgres', 'password': 'postgres', 'port': '5432'},
            {'host': 'localhost', 'database': 'postgres', 'user': 'postgres', 'password': 'postgres', 'port': '5432', 'client_encoding': 'UTF8'},
            {'host': 'localhost', 'database': 'postgres', 'user': 'postgres', 'password': 'postgres', 'port': '5432', 'client_encoding': 'LATIN1'},
        ]
        
        for i, config in enumerate(configuraciones):
            try:
                print(f"  Probando configuración {i+1}: {config}")
                conn = psycopg2.connect(**config)
                print(f"  ✅ Configuración {i+1} exitosa")
                conn.close()
                return True
            except Exception as e:
                print(f"  ❌ Configuración {i+1} falló: {e}")
        
        return False
    except Exception as e:
        print(f"❌ Error en psycopg2: {e}")
        return False

def verificar_configuracion_postgresql():
    """Verifica la configuración de PostgreSQL"""
    print("\n🔍 Verificando configuración de PostgreSQL...")
    
    try:
        # Verificar configuración de PostgreSQL
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ PostgreSQL versión: {result.stdout.strip()}")
        else:
            print(f"❌ Error obteniendo versión de PostgreSQL: {result.stderr}")
            return False
        
        # Verificar configuración de encoding
        result = subprocess.run(['psql', '-U', 'postgres', '-c', 'SHOW client_encoding;'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ Client encoding: {result.stdout.strip()}")
        else:
            print(f"❌ Error obteniendo client encoding: {result.stderr}")
        
        # Verificar configuración de server encoding
        result = subprocess.run(['psql', '-U', 'postgres', '-c', 'SHOW server_encoding;'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ Server encoding: {result.stdout.strip()}")
        else:
            print(f"❌ Error obteniendo server encoding: {result.stderr}")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def probar_conexion_con_dsn():
    """Prueba la conexión usando DSN"""
    print("\n🔍 Probando conexión con DSN...")
    
    try:
        import psycopg2
        
        # Probar con DSN string
        dsn_strings = [
            "host=localhost dbname=postgres user=postgres password=postgres port=5432",
            "host=127.0.0.1 dbname=postgres user=postgres password=postgres port=5432",
            "host=localhost dbname=postgres user=postgres password=postgres port=5432 client_encoding=UTF8",
        ]
        
        for i, dsn in enumerate(dsn_strings):
            try:
                print(f"  Probando DSN {i+1}: {dsn}")
                conn = psycopg2.connect(dsn)
                print(f"  ✅ DSN {i+1} exitoso")
                conn.close()
                return True
            except Exception as e:
                print(f"  ❌ DSN {i+1} falló: {e}")
        
        return False
    except Exception as e:
        print(f"❌ Error probando DSN: {e}")
        return False

def verificar_variables_entorno():
    """Verifica las variables de entorno"""
    print("\n🔍 Verificando variables de entorno...")
    
    variables = ['PGHOST', 'PGPORT', 'PGUSER', 'PGPASSWORD', 'PGDATABASE', 'PGCLIENTENCODING']
    
    for var in variables:
        value = os.environ.get(var, 'No definida')
        print(f"  {var}: {value}")
    
    return True

def main():
    """Función principal de debug"""
    print("🚀 Iniciando debug específico de psycopg2...")
    
    # Paso 1: Verificar versión de psycopg2
    if not verificar_version_psycopg2():
        print("❌ No se puede importar psycopg2")
        return
    
    # Paso 2: Verificar variables de entorno
    verificar_variables_entorno()
    
    # Paso 3: Verificar configuración de PostgreSQL
    verificar_configuracion_postgresql()
    
    # Paso 4: Probar conexión con diferentes encodings
    if probar_conexion_con_diferentes_encodings():
        print("\n🎉 ¡Se encontró una configuración que funciona!")
        return
    
    # Paso 5: Probar conexión con DSN
    if probar_conexion_con_dsn():
        print("\n🎉 ¡Se encontró una configuración DSN que funciona!")
        return
    
    print("\n❌ No se encontró ninguna configuración que funcione")
    print("\n📋 Posibles soluciones:")
    print("1. Reinstalar psycopg2: pip uninstall psycopg2-binary && pip install psycopg2-binary")
    print("2. Verificar configuración de PostgreSQL")
    print("3. Usar una versión diferente de psycopg2")

if __name__ == "__main__":
    main()

"""
Script para debuggear específicamente psycopg2
"""
import os
import sys
import subprocess

def verificar_version_psycopg2():
    """Verifica la versión de psycopg2"""
    print("🔍 Verificando versión de psycopg2...")
    try:
        import psycopg2
        print(f"✅ psycopg2 versión: {psycopg2.__version__}")
        return True
    except Exception as e:
        print(f"❌ Error importando psycopg2: {e}")
        return False

def probar_conexion_con_diferentes_encodings():
    """Prueba la conexión con diferentes encodings"""
    print("\n🔍 Probando conexión con diferentes encodings...")
    
    try:
        import psycopg2
        
        # Probar con diferentes configuraciones de encoding
        configuraciones = [
            {'host': 'localhost', 'database': 'postgres', 'user': 'postgres', 'password': 'postgres', 'port': '5432'},
            {'host': '127.0.0.1', 'database': 'postgres', 'user': 'postgres', 'password': 'postgres', 'port': '5432'},
            {'host': 'localhost', 'database': 'postgres', 'user': 'postgres', 'password': 'postgres', 'port': '5432', 'client_encoding': 'UTF8'},
            {'host': 'localhost', 'database': 'postgres', 'user': 'postgres', 'password': 'postgres', 'port': '5432', 'client_encoding': 'LATIN1'},
        ]
        
        for i, config in enumerate(configuraciones):
            try:
                print(f"  Probando configuración {i+1}: {config}")
                conn = psycopg2.connect(**config)
                print(f"  ✅ Configuración {i+1} exitosa")
                conn.close()
                return True
            except Exception as e:
                print(f"  ❌ Configuración {i+1} falló: {e}")
        
        return False
    except Exception as e:
        print(f"❌ Error en psycopg2: {e}")
        return False

def verificar_configuracion_postgresql():
    """Verifica la configuración de PostgreSQL"""
    print("\n🔍 Verificando configuración de PostgreSQL...")
    
    try:
        # Verificar configuración de PostgreSQL
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ PostgreSQL versión: {result.stdout.strip()}")
        else:
            print(f"❌ Error obteniendo versión de PostgreSQL: {result.stderr}")
            return False
        
        # Verificar configuración de encoding
        result = subprocess.run(['psql', '-U', 'postgres', '-c', 'SHOW client_encoding;'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ Client encoding: {result.stdout.strip()}")
        else:
            print(f"❌ Error obteniendo client encoding: {result.stderr}")
        
        # Verificar configuración de server encoding
        result = subprocess.run(['psql', '-U', 'postgres', '-c', 'SHOW server_encoding;'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ Server encoding: {result.stdout.strip()}")
        else:
            print(f"❌ Error obteniendo server encoding: {result.stderr}")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def probar_conexion_con_dsn():
    """Prueba la conexión usando DSN"""
    print("\n🔍 Probando conexión con DSN...")
    
    try:
        import psycopg2
        
        # Probar con DSN string
        dsn_strings = [
            "host=localhost dbname=postgres user=postgres password=postgres port=5432",
            "host=127.0.0.1 dbname=postgres user=postgres password=postgres port=5432",
            "host=localhost dbname=postgres user=postgres password=postgres port=5432 client_encoding=UTF8",
        ]
        
        for i, dsn in enumerate(dsn_strings):
            try:
                print(f"  Probando DSN {i+1}: {dsn}")
                conn = psycopg2.connect(dsn)
                print(f"  ✅ DSN {i+1} exitoso")
                conn.close()
                return True
            except Exception as e:
                print(f"  ❌ DSN {i+1} falló: {e}")
        
        return False
    except Exception as e:
        print(f"❌ Error probando DSN: {e}")
        return False

def verificar_variables_entorno():
    """Verifica las variables de entorno"""
    print("\n🔍 Verificando variables de entorno...")
    
    variables = ['PGHOST', 'PGPORT', 'PGUSER', 'PGPASSWORD', 'PGDATABASE', 'PGCLIENTENCODING']
    
    for var in variables:
        value = os.environ.get(var, 'No definida')
        print(f"  {var}: {value}")
    
    return True

def main():
    """Función principal de debug"""
    print("🚀 Iniciando debug específico de psycopg2...")
    
    # Paso 1: Verificar versión de psycopg2
    if not verificar_version_psycopg2():
        print("❌ No se puede importar psycopg2")
        return
    
    # Paso 2: Verificar variables de entorno
    verificar_variables_entorno()
    
    # Paso 3: Verificar configuración de PostgreSQL
    verificar_configuracion_postgresql()
    
    # Paso 4: Probar conexión con diferentes encodings
    if probar_conexion_con_diferentes_encodings():
        print("\n🎉 ¡Se encontró una configuración que funciona!")
        return
    
    # Paso 5: Probar conexión con DSN
    if probar_conexion_con_dsn():
        print("\n🎉 ¡Se encontró una configuración DSN que funciona!")
        return
    
    print("\n❌ No se encontró ninguna configuración que funcione")
    print("\n📋 Posibles soluciones:")
    print("1. Reinstalar psycopg2: pip uninstall psycopg2-binary && pip install psycopg2-binary")
    print("2. Verificar configuración de PostgreSQL")
    print("3. Usar una versión diferente de psycopg2")

if __name__ == "__main__":
    main()




