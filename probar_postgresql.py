#!/usr/bin/env python
"""
Script simplificado para probar PostgreSQL
"""

import os
import subprocess

def configurar_path():
    """Configurar PATH para PostgreSQL"""
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        return True
    return False

def probar_psql():
    """Probar psql"""
    print("🔍 Probando psql...")
    try:
        result = subprocess.run('psql --version', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ psql funcionando: {result.stdout.strip()}")
            return True
        else:
            print("❌ psql no funciona")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def probar_conexion():
    """Probar conexión a PostgreSQL"""
    print("🔗 Probando conexión a PostgreSQL...")
    
    # Solicitar contraseña
    password = input("Ingresa la contraseña del usuario 'postgres': ")
    
    if not password:
        print("❌ No se ingresó contraseña")
        return False
    
    try:
        # Configurar contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        # Probar conexión
        result = subprocess.run(
            'psql -U postgres -d postgres -c "SELECT version();"',
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print("✅ Conexión exitosa a PostgreSQL")
            print(f"📊 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error de conexión: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🐘 PROBADOR DE POSTGRESQL")
    print("=" * 30)
    
    # Configurar PATH
    if not configurar_path():
        print("❌ No se pudo configurar PATH")
        return False
    
    # Probar psql
    if not probar_psql():
        print("❌ psql no está disponible")
        return False
    
    # Probar conexión
    if probar_conexion():
        print("\n🎉 PostgreSQL está funcionando correctamente")
        print("   Puedes continuar con la migración")
        return True
    else:
        print("\n❌ Hay problemas con PostgreSQL")
        return False

if __name__ == "__main__":
    main()


"""
Script simplificado para probar PostgreSQL
"""

import os
import subprocess

def configurar_path():
    """Configurar PATH para PostgreSQL"""
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        return True
    return False

def probar_psql():
    """Probar psql"""
    print("🔍 Probando psql...")
    try:
        result = subprocess.run('psql --version', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ psql funcionando: {result.stdout.strip()}")
            return True
        else:
            print("❌ psql no funciona")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def probar_conexion():
    """Probar conexión a PostgreSQL"""
    print("🔗 Probando conexión a PostgreSQL...")
    
    # Solicitar contraseña
    password = input("Ingresa la contraseña del usuario 'postgres': ")
    
    if not password:
        print("❌ No se ingresó contraseña")
        return False
    
    try:
        # Configurar contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        # Probar conexión
        result = subprocess.run(
            'psql -U postgres -d postgres -c "SELECT version();"',
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print("✅ Conexión exitosa a PostgreSQL")
            print(f"📊 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error de conexión: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🐘 PROBADOR DE POSTGRESQL")
    print("=" * 30)
    
    # Configurar PATH
    if not configurar_path():
        print("❌ No se pudo configurar PATH")
        return False
    
    # Probar psql
    if not probar_psql():
        print("❌ psql no está disponible")
        return False
    
    # Probar conexión
    if probar_conexion():
        print("\n🎉 PostgreSQL está funcionando correctamente")
        print("   Puedes continuar con la migración")
        return True
    else:
        print("\n❌ Hay problemas con PostgreSQL")
        return False

if __name__ == "__main__":
    main()







