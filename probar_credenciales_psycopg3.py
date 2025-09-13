#!/usr/bin/env python
"""
Script para probar diferentes credenciales de PostgreSQL con psycopg3
"""

import psycopg

def probar_conexion(host, port, user, password, dbname):
    """Probar conexión con credenciales específicas"""
    try:
        conn = psycopg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        print(f"✅ Conexión exitosa: {user}@{host}:{port}/{dbname}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error: {user}@{host}:{port}/{dbname} - {e}")
        return False

def main():
    """Probar diferentes combinaciones de credenciales"""
    print("🔍 Probando credenciales de PostgreSQL con psycopg3")
    print("=" * 60)
    
    # Lista de credenciales a probar
    credenciales = [
        # (host, port, user, password, dbname)
        ("127.0.0.1", "5432", "postgres", "", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "postgres", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "admin", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "123456", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "password", "kreadental_cloud"),
        ("localhost", "5432", "postgres", "", "kreadental_cloud"),
        ("localhost", "5432", "postgres", "postgres", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "", "postgres"),
        ("127.0.0.1", "5432", "postgres", "postgres", "postgres"),
    ]
    
    conexiones_exitosas = 0
    
    for host, port, user, password, dbname in credenciales:
        if probar_conexion(host, port, user, password, dbname):
            conexiones_exitosas += 1
            print(f"🎉 ¡Credenciales encontradas: {user}@{host}:{port}/{dbname}")
            break
    
    if conexiones_exitosas == 0:
        print("\n❌ No se encontraron credenciales válidas")
        print("💡 Sugerencias:")
        print("   1. Verificar que PostgreSQL esté ejecutándose")
        print("   2. Verificar la contraseña del usuario postgres")
        print("   3. Verificar que la base de datos exista")
        print("   4. Verificar la configuración de pg_hba.conf")
    
    return conexiones_exitosas > 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

"""
Script para probar diferentes credenciales de PostgreSQL con psycopg3
"""

import psycopg

def probar_conexion(host, port, user, password, dbname):
    """Probar conexión con credenciales específicas"""
    try:
        conn = psycopg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        print(f"✅ Conexión exitosa: {user}@{host}:{port}/{dbname}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error: {user}@{host}:{port}/{dbname} - {e}")
        return False

def main():
    """Probar diferentes combinaciones de credenciales"""
    print("🔍 Probando credenciales de PostgreSQL con psycopg3")
    print("=" * 60)
    
    # Lista de credenciales a probar
    credenciales = [
        # (host, port, user, password, dbname)
        ("127.0.0.1", "5432", "postgres", "", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "postgres", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "admin", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "123456", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "password", "kreadental_cloud"),
        ("localhost", "5432", "postgres", "", "kreadental_cloud"),
        ("localhost", "5432", "postgres", "postgres", "kreadental_cloud"),
        ("127.0.0.1", "5432", "postgres", "", "postgres"),
        ("127.0.0.1", "5432", "postgres", "postgres", "postgres"),
    ]
    
    conexiones_exitosas = 0
    
    for host, port, user, password, dbname in credenciales:
        if probar_conexion(host, port, user, password, dbname):
            conexiones_exitosas += 1
            print(f"🎉 ¡Credenciales encontradas: {user}@{host}:{port}/{dbname}")
            break
    
    if conexiones_exitosas == 0:
        print("\n❌ No se encontraron credenciales válidas")
        print("💡 Sugerencias:")
        print("   1. Verificar que PostgreSQL esté ejecutándose")
        print("   2. Verificar la contraseña del usuario postgres")
        print("   3. Verificar que la base de datos exista")
        print("   4. Verificar la configuración de pg_hba.conf")
    
    return conexiones_exitosas > 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)






