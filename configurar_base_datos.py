#!/usr/bin/env python
"""
Script para configurar la base de datos PostgreSQL
"""

import os
import subprocess
import getpass
from dotenv import load_dotenv

def configurar_path_sesion():
    """Configurar PATH para la sesión actual"""
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        return True
    return False

def probar_conexion(password):
    """Probar conexión con una contraseña"""
    try:
        # Usar PGPASSWORD para evitar prompt interactivo
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        result = subprocess.run(
            'psql -U postgres -d postgres -c "SELECT version();"',
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except Exception as e:
        return False, str(e)

def configurar_contrasena():
    """Configurar contraseña de PostgreSQL"""
    print("🔐 Configuración de contraseña de PostgreSQL")
    print("=" * 50)
    
    # Cargar configuración actual
    load_dotenv()
    current_password = os.getenv('DB_PASSWORD', '')
    
    if current_password:
        print(f"📝 Contraseña actual en .env: {current_password}")
        
        # Probar contraseña actual
        print("🔍 Probando contraseña actual...")
        success, output = probar_conexion(current_password)
        
        if success:
            print("✅ Contraseña actual funciona correctamente")
            return current_password
        else:
            print(f"❌ Contraseña actual no funciona: {output}")
    
    # Solicitar nueva contraseña
    print("\n🔑 Ingresa la contraseña del usuario 'postgres':")
    password = getpass.getpass("Contraseña: ")
    
    if not password:
        print("❌ No se ingresó contraseña")
        return None
    
    # Probar nueva contraseña
    print("🔍 Probando nueva contraseña...")
    success, output = probar_conexion(password)
    
    if success:
        print("✅ Contraseña correcta")
        
        # Actualizar .env
        actualizar_env_password(password)
        return password
    else:
        print(f"❌ Contraseña incorrecta: {output}")
        return None

def actualizar_env_password(password):
    """Actualizar contraseña en archivo .env"""
    print("📝 Actualizando archivo .env...")
    
    try:
        # Leer archivo .env
        with open('.env', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Actualizar contraseña
        updated_lines = []
        for line in lines:
            if line.startswith('DB_PASSWORD='):
                updated_lines.append(f'DB_PASSWORD={password}\n')
            else:
                updated_lines.append(line)
        
        # Escribir archivo actualizado
        with open('.env', 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        print("✅ Archivo .env actualizado")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando .env: {e}")
        return False

def crear_base_datos():
    """Crear base de datos para KreaDental Cloud"""
    print("🗄️  Creando base de datos...")
    
    try:
        # Cargar configuración
        load_dotenv()
        db_name = os.getenv('DB_NAME', 'kreadental_cloud')
        password = os.getenv('DB_PASSWORD', '')
        
        if not password:
            print("❌ No hay contraseña configurada")
            return False
        
        # Configurar entorno
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        # Crear base de datos
        result = subprocess.run(
            f'psql -U postgres -d postgres -c "CREATE DATABASE \\"{db_name}\\" WITH ENCODING=\'UTF8\';"',
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print(f"✅ Base de datos '{db_name}' creada exitosamente")
            return True
        else:
            # Verificar si ya existe
            if "already exists" in result.stderr:
                print(f"ℹ️  La base de datos '{db_name}' ya existe")
                return True
            else:
                print(f"❌ Error creando base de datos: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def verificar_base_datos():
    """Verificar que la base de datos esté funcionando"""
    print("🔍 Verificando base de datos...")
    
    try:
        # Cargar configuración
        load_dotenv()
        db_name = os.getenv('DB_NAME', 'kreadental_cloud')
        password = os.getenv('DB_PASSWORD', '')
        
        if not password:
            print("❌ No hay contraseña configurada")
            return False
        
        # Configurar entorno
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        # Verificar conexión a la base de datos
        result = subprocess.run(
            f'psql -U postgres -d {db_name} -c "SELECT current_database(), current_user;"',
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print("✅ Base de datos funcionando correctamente")
            print(f"   📊 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error verificando base de datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("🗄️  CONFIGURADOR DE BASE DE DATOS POSTGRESQL")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Configurar PATH
    if not configurar_path_sesion():
        print("❌ No se pudo configurar PATH de PostgreSQL")
        return False
    
    # Configurar contraseña
    password = configurar_contrasena()
    if not password:
        print("❌ No se pudo configurar la contraseña")
        return False
    
    # Crear base de datos
    if not crear_base_datos():
        print("❌ No se pudo crear la base de datos")
        return False
    
    # Verificar base de datos
    if not verificar_base_datos():
        print("❌ La base de datos no está funcionando correctamente")
        return False
    
    print("\n🎉 ¡Base de datos configurada exitosamente!")
    print("   PostgreSQL está listo para KreaDental Cloud")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n📝 Próximos pasos:")
        print("1. python verificar_sistema.py")
        print("2. python migrate_to_postgresql.py")
    else:
        print("\n❌ Hay problemas que resolver antes de continuar")


"""
Script para configurar la base de datos PostgreSQL
"""

import os
import subprocess
import getpass
from dotenv import load_dotenv

def configurar_path_sesion():
    """Configurar PATH para la sesión actual"""
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    if os.path.exists(postgresql_bin):
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
        return True
    return False

def probar_conexion(password):
    """Probar conexión con una contraseña"""
    try:
        # Usar PGPASSWORD para evitar prompt interactivo
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        result = subprocess.run(
            'psql -U postgres -d postgres -c "SELECT version();"',
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
            
    except Exception as e:
        return False, str(e)

def configurar_contrasena():
    """Configurar contraseña de PostgreSQL"""
    print("🔐 Configuración de contraseña de PostgreSQL")
    print("=" * 50)
    
    # Cargar configuración actual
    load_dotenv()
    current_password = os.getenv('DB_PASSWORD', '')
    
    if current_password:
        print(f"📝 Contraseña actual en .env: {current_password}")
        
        # Probar contraseña actual
        print("🔍 Probando contraseña actual...")
        success, output = probar_conexion(current_password)
        
        if success:
            print("✅ Contraseña actual funciona correctamente")
            return current_password
        else:
            print(f"❌ Contraseña actual no funciona: {output}")
    
    # Solicitar nueva contraseña
    print("\n🔑 Ingresa la contraseña del usuario 'postgres':")
    password = getpass.getpass("Contraseña: ")
    
    if not password:
        print("❌ No se ingresó contraseña")
        return None
    
    # Probar nueva contraseña
    print("🔍 Probando nueva contraseña...")
    success, output = probar_conexion(password)
    
    if success:
        print("✅ Contraseña correcta")
        
        # Actualizar .env
        actualizar_env_password(password)
        return password
    else:
        print(f"❌ Contraseña incorrecta: {output}")
        return None

def actualizar_env_password(password):
    """Actualizar contraseña en archivo .env"""
    print("📝 Actualizando archivo .env...")
    
    try:
        # Leer archivo .env
        with open('.env', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Actualizar contraseña
        updated_lines = []
        for line in lines:
            if line.startswith('DB_PASSWORD='):
                updated_lines.append(f'DB_PASSWORD={password}\n')
            else:
                updated_lines.append(line)
        
        # Escribir archivo actualizado
        with open('.env', 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        print("✅ Archivo .env actualizado")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando .env: {e}")
        return False

def crear_base_datos():
    """Crear base de datos para KreaDental Cloud"""
    print("🗄️  Creando base de datos...")
    
    try:
        # Cargar configuración
        load_dotenv()
        db_name = os.getenv('DB_NAME', 'kreadental_cloud')
        password = os.getenv('DB_PASSWORD', '')
        
        if not password:
            print("❌ No hay contraseña configurada")
            return False
        
        # Configurar entorno
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        # Crear base de datos
        result = subprocess.run(
            f'psql -U postgres -d postgres -c "CREATE DATABASE \\"{db_name}\\" WITH ENCODING=\'UTF8\';"',
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print(f"✅ Base de datos '{db_name}' creada exitosamente")
            return True
        else:
            # Verificar si ya existe
            if "already exists" in result.stderr:
                print(f"ℹ️  La base de datos '{db_name}' ya existe")
                return True
            else:
                print(f"❌ Error creando base de datos: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def verificar_base_datos():
    """Verificar que la base de datos esté funcionando"""
    print("🔍 Verificando base de datos...")
    
    try:
        # Cargar configuración
        load_dotenv()
        db_name = os.getenv('DB_NAME', 'kreadental_cloud')
        password = os.getenv('DB_PASSWORD', '')
        
        if not password:
            print("❌ No hay contraseña configurada")
            return False
        
        # Configurar entorno
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        # Verificar conexión a la base de datos
        result = subprocess.run(
            f'psql -U postgres -d {db_name} -c "SELECT current_database(), current_user;"',
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print("✅ Base de datos funcionando correctamente")
            print(f"   📊 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error verificando base de datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("🗄️  CONFIGURADOR DE BASE DE DATOS POSTGRESQL")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Configurar PATH
    if not configurar_path_sesion():
        print("❌ No se pudo configurar PATH de PostgreSQL")
        return False
    
    # Configurar contraseña
    password = configurar_contrasena()
    if not password:
        print("❌ No se pudo configurar la contraseña")
        return False
    
    # Crear base de datos
    if not crear_base_datos():
        print("❌ No se pudo crear la base de datos")
        return False
    
    # Verificar base de datos
    if not verificar_base_datos():
        print("❌ La base de datos no está funcionando correctamente")
        return False
    
    print("\n🎉 ¡Base de datos configurada exitosamente!")
    print("   PostgreSQL está listo para KreaDental Cloud")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n📝 Próximos pasos:")
        print("1. python verificar_sistema.py")
        print("2. python migrate_to_postgresql.py")
    else:
        print("\n❌ Hay problemas que resolver antes de continuar")







