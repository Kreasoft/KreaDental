#!/usr/bin/env python
"""
Script para probar contraseñas comunes de PostgreSQL
"""

import os
import subprocess

def configurar_path():
    """Configurar PATH de PostgreSQL"""
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        return True
    return False

def probar_contrasena(password):
    """Probar una contraseña específica"""
    try:
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'SELECT version();'
        ], capture_output=True, text=True, env=env)
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except Exception as e:
        return False, str(e)

def main():
    print("🔐 PROBADOR DE CONTRASEÑAS DE POSTGRESQL")
    print("=" * 50)
    
    # Configurar PATH
    if not configurar_path():
        print("❌ No se pudo configurar PATH de PostgreSQL")
        return
    
    # Contraseñas comunes a probar
    contrasenas_comunes = [
        "postgres",
        "postgres123",
        "admin",
        "password",
        "123456",
        "root",
        "postgresql",
        "postgres2024",
        "postgres2023",
        "postgres2022",
        "kreasoft",
        "kreadental",
        "",
    ]
    
    print("🔍 Probando contraseñas comunes...")
    print("-" * 30)
    
    for i, password in enumerate(contrasenas_comunes, 1):
        print(f"{i:2d}. Probando: {'(vacía)' if password == '' else password}")
        
        success, output = probar_contrasena(password)
        
        if success:
            print(f"✅ ¡CONTRASEÑA ENCONTRADA!")
            print(f"   Contraseña: {password if password else '(vacía)'}")
            print(f"   Versión: {output.strip()}")
            
            # Actualizar archivo .env
            actualizar_env(password)
            return True
        else:
            print(f"   ❌ No funciona")
    
    print("\n❌ Ninguna contraseña común funcionó")
    print("\n💡 OPCIONES:")
    print("1. Reinstalar PostgreSQL con contraseña conocida")
    print("2. Resetear contraseña de PostgreSQL")
    print("3. Usar autenticación de Windows")
    
    return False

def actualizar_env(password):
    """Actualizar archivo .env con la contraseña encontrada"""
    print("\n📝 Actualizando archivo .env...")
    
    env_content = f"""# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD={password}
DB_HOST=localhost
DB_PORT=5432

# Configuración de Django
SECRET_KEY=kreasoft-52432cl+
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env actualizado con la contraseña correcta")
    except Exception as e:
        print(f"❌ Error actualizando .env: {e}")

if __name__ == "__main__":
    main()


"""
Script para probar contraseñas comunes de PostgreSQL
"""

import os
import subprocess

def configurar_path():
    """Configurar PATH de PostgreSQL"""
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        return True
    return False

def probar_contrasena(password):
    """Probar una contraseña específica"""
    try:
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'SELECT version();'
        ], capture_output=True, text=True, env=env)
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except Exception as e:
        return False, str(e)

def main():
    print("🔐 PROBADOR DE CONTRASEÑAS DE POSTGRESQL")
    print("=" * 50)
    
    # Configurar PATH
    if not configurar_path():
        print("❌ No se pudo configurar PATH de PostgreSQL")
        return
    
    # Contraseñas comunes a probar
    contrasenas_comunes = [
        "postgres",
        "postgres123",
        "admin",
        "password",
        "123456",
        "root",
        "postgresql",
        "postgres2024",
        "postgres2023",
        "postgres2022",
        "kreasoft",
        "kreadental",
        "",
    ]
    
    print("🔍 Probando contraseñas comunes...")
    print("-" * 30)
    
    for i, password in enumerate(contrasenas_comunes, 1):
        print(f"{i:2d}. Probando: {'(vacía)' if password == '' else password}")
        
        success, output = probar_contrasena(password)
        
        if success:
            print(f"✅ ¡CONTRASEÑA ENCONTRADA!")
            print(f"   Contraseña: {password if password else '(vacía)'}")
            print(f"   Versión: {output.strip()}")
            
            # Actualizar archivo .env
            actualizar_env(password)
            return True
        else:
            print(f"   ❌ No funciona")
    
    print("\n❌ Ninguna contraseña común funcionó")
    print("\n💡 OPCIONES:")
    print("1. Reinstalar PostgreSQL con contraseña conocida")
    print("2. Resetear contraseña de PostgreSQL")
    print("3. Usar autenticación de Windows")
    
    return False

def actualizar_env(password):
    """Actualizar archivo .env con la contraseña encontrada"""
    print("\n📝 Actualizando archivo .env...")
    
    env_content = f"""# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD={password}
DB_HOST=localhost
DB_PORT=5432

# Configuración de Django
SECRET_KEY=kreasoft-52432cl+
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env actualizado con la contraseña correcta")
    except Exception as e:
        print(f"❌ Error actualizando .env: {e}")

if __name__ == "__main__":
    main()











