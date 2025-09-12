#!/usr/bin/env python
"""
Script para configurar la autenticación de PostgreSQL
"""

import subprocess
import os
import sys

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"🔧 {descripcion}")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0:
            print(f"✅ {descripcion} - Exitoso")
            if result.stdout.strip():
                print(f"   Salida: {result.stdout.strip()}")
        else:
            print(f"❌ {descripcion} - Error")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {descripcion} - Excepción: {e}")
        return False

def encontrar_postgresql():
    """Encontrar la instalación de PostgreSQL"""
    posibles_rutas = [
        r"C:\Program Files\PostgreSQL\17\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\15\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\14\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\13\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\12\bin\psql.exe",
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            print(f"✅ PostgreSQL encontrado en: {ruta}")
            return ruta
    
    print("❌ PostgreSQL no encontrado en las rutas estándar")
    return None

def configurar_autenticacion():
    """Configurar la autenticación de PostgreSQL"""
    print("🔧 Configurando autenticación de PostgreSQL")
    print("=" * 50)
    
    # 1. Encontrar PostgreSQL
    psql_path = encontrar_postgresql()
    if not psql_path:
        print("❌ No se pudo encontrar PostgreSQL")
        return False
    
    # 2. Intentar conectar sin contraseña (trust)
    print("\n🔍 Probando conexión sin contraseña...")
    comando_trust = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "SELECT version();"'
    if ejecutar_comando(comando_trust, "Conexión con trust"):
        print("✅ PostgreSQL configurado con autenticación trust")
        return True
    
    # 3. Intentar con contraseña vacía
    print("\n🔍 Probando con contraseña vacía...")
    comando_vacio = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "SELECT version();"'
    if ejecutar_comando(comando_vacio, "Conexión con contraseña vacía"):
        print("✅ PostgreSQL acepta contraseña vacía")
        return True
    
    # 4. Intentar cambiar contraseña
    print("\n🔍 Intentando cambiar contraseña...")
    comando_cambiar = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "ALTER USER postgres PASSWORD \'postgres\';"'
    if ejecutar_comando(comando_cambiar, "Cambiar contraseña a 'postgres'"):
        print("✅ Contraseña cambiada a 'postgres'")
        return True
    
    print("❌ No se pudo configurar la autenticación automáticamente")
    print("\n💡 Instrucciones manuales:")
    print("   1. Abre pgAdmin o psql")
    print("   2. Conecta como superusuario")
    print("   3. Ejecuta: ALTER USER postgres PASSWORD 'postgres';")
    print("   4. O configura pg_hba.conf para usar 'trust'")
    
    return False

def crear_base_datos():
    """Crear la base de datos si no existe"""
    print("\n🔧 Creando base de datos")
    print("=" * 30)
    
    psql_path = encontrar_postgresql()
    if not psql_path:
        return False
    
    # Crear base de datos
    comando_crear = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "CREATE DATABASE kreadental_cloud;"'
    if ejecutar_comando(comando_crear, "Crear base de datos kreadental_cloud"):
        print("✅ Base de datos creada")
        return True
    
    # Verificar si ya existe
    comando_verificar = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "SELECT datname FROM pg_database WHERE datname = \'kreadental_cloud\';"'
    if ejecutar_comando(comando_verificar, "Verificar si existe kreadental_cloud"):
        print("✅ Base de datos ya existe")
        return True
    
    return False

def probar_conexion_final():
    """Probar la conexión final"""
    print("\n🔍 Probando conexión final")
    print("=" * 30)
    
    psql_path = encontrar_postgresql()
    if not psql_path:
        return False
    
    comando_probar = f'"{psql_path}" -U postgres -h localhost -p 5432 -d kreadental_cloud -c "SELECT current_database(), current_user;"'
    return ejecutar_comando(comando_probar, "Conexión final a kreadental_cloud")

def main():
    """Función principal"""
    print("🚀 Configurando PostgreSQL para migración")
    print("=" * 50)
    
    # 1. Configurar autenticación
    if not configurar_autenticacion():
        print("❌ No se pudo configurar la autenticación")
        return False
    
    # 2. Crear base de datos
    if not crear_base_datos():
        print("❌ No se pudo crear la base de datos")
        return False
    
    # 3. Probar conexión final
    if not probar_conexion_final():
        print("❌ No se pudo conectar a la base de datos final")
        return False
    
    print("\n🎉 ¡PostgreSQL configurado correctamente!")
    print("✅ Listo para migrar datos")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

"""
Script para configurar la autenticación de PostgreSQL
"""

import subprocess
import os
import sys

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"🔧 {descripcion}")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0:
            print(f"✅ {descripcion} - Exitoso")
            if result.stdout.strip():
                print(f"   Salida: {result.stdout.strip()}")
        else:
            print(f"❌ {descripcion} - Error")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {descripcion} - Excepción: {e}")
        return False

def encontrar_postgresql():
    """Encontrar la instalación de PostgreSQL"""
    posibles_rutas = [
        r"C:\Program Files\PostgreSQL\17\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\15\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\14\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\13\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\12\bin\psql.exe",
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            print(f"✅ PostgreSQL encontrado en: {ruta}")
            return ruta
    
    print("❌ PostgreSQL no encontrado en las rutas estándar")
    return None

def configurar_autenticacion():
    """Configurar la autenticación de PostgreSQL"""
    print("🔧 Configurando autenticación de PostgreSQL")
    print("=" * 50)
    
    # 1. Encontrar PostgreSQL
    psql_path = encontrar_postgresql()
    if not psql_path:
        print("❌ No se pudo encontrar PostgreSQL")
        return False
    
    # 2. Intentar conectar sin contraseña (trust)
    print("\n🔍 Probando conexión sin contraseña...")
    comando_trust = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "SELECT version();"'
    if ejecutar_comando(comando_trust, "Conexión con trust"):
        print("✅ PostgreSQL configurado con autenticación trust")
        return True
    
    # 3. Intentar con contraseña vacía
    print("\n🔍 Probando con contraseña vacía...")
    comando_vacio = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "SELECT version();"'
    if ejecutar_comando(comando_vacio, "Conexión con contraseña vacía"):
        print("✅ PostgreSQL acepta contraseña vacía")
        return True
    
    # 4. Intentar cambiar contraseña
    print("\n🔍 Intentando cambiar contraseña...")
    comando_cambiar = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "ALTER USER postgres PASSWORD \'postgres\';"'
    if ejecutar_comando(comando_cambiar, "Cambiar contraseña a 'postgres'"):
        print("✅ Contraseña cambiada a 'postgres'")
        return True
    
    print("❌ No se pudo configurar la autenticación automáticamente")
    print("\n💡 Instrucciones manuales:")
    print("   1. Abre pgAdmin o psql")
    print("   2. Conecta como superusuario")
    print("   3. Ejecuta: ALTER USER postgres PASSWORD 'postgres';")
    print("   4. O configura pg_hba.conf para usar 'trust'")
    
    return False

def crear_base_datos():
    """Crear la base de datos si no existe"""
    print("\n🔧 Creando base de datos")
    print("=" * 30)
    
    psql_path = encontrar_postgresql()
    if not psql_path:
        return False
    
    # Crear base de datos
    comando_crear = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "CREATE DATABASE kreadental_cloud;"'
    if ejecutar_comando(comando_crear, "Crear base de datos kreadental_cloud"):
        print("✅ Base de datos creada")
        return True
    
    # Verificar si ya existe
    comando_verificar = f'"{psql_path}" -U postgres -h localhost -p 5432 -d postgres -c "SELECT datname FROM pg_database WHERE datname = \'kreadental_cloud\';"'
    if ejecutar_comando(comando_verificar, "Verificar si existe kreadental_cloud"):
        print("✅ Base de datos ya existe")
        return True
    
    return False

def probar_conexion_final():
    """Probar la conexión final"""
    print("\n🔍 Probando conexión final")
    print("=" * 30)
    
    psql_path = encontrar_postgresql()
    if not psql_path:
        return False
    
    comando_probar = f'"{psql_path}" -U postgres -h localhost -p 5432 -d kreadental_cloud -c "SELECT current_database(), current_user;"'
    return ejecutar_comando(comando_probar, "Conexión final a kreadental_cloud")

def main():
    """Función principal"""
    print("🚀 Configurando PostgreSQL para migración")
    print("=" * 50)
    
    # 1. Configurar autenticación
    if not configurar_autenticacion():
        print("❌ No se pudo configurar la autenticación")
        return False
    
    # 2. Crear base de datos
    if not crear_base_datos():
        print("❌ No se pudo crear la base de datos")
        return False
    
    # 3. Probar conexión final
    if not probar_conexion_final():
        print("❌ No se pudo conectar a la base de datos final")
        return False
    
    print("\n🎉 ¡PostgreSQL configurado correctamente!")
    print("✅ Listo para migrar datos")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




