#!/usr/bin/env python
"""
Script para configurar PostgreSQL sin contraseña
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

def configurar_postgresql_sin_contrasena():
    """Configurar PostgreSQL para autenticación sin contraseña"""
    print("🔧 Configurando PostgreSQL para autenticación sin contraseña...")
    
    # Ruta del archivo pg_hba.conf
    pg_hba_path = "C:\\Program Files\\PostgreSQL\\17\\data\\pg_hba.conf"
    
    if not os.path.exists(pg_hba_path):
        print(f"❌ No se encontró pg_hba.conf en: {pg_hba_path}")
        print("   Busca el archivo pg_hba.conf en tu instalación de PostgreSQL")
        return False
    
    print(f"✅ Archivo pg_hba.conf encontrado: {pg_hba_path}")
    
    # Leer archivo actual
    try:
        with open(pg_hba_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error leyendo pg_hba.conf: {e}")
        return False
    
    # Buscar línea de autenticación local
    modified = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('local') and 'all' in line and 'postgres' in line:
            # Cambiar de md5 a trust para autenticación sin contraseña
            if 'md5' in line:
                new_line = line.replace('md5', 'trust')
                new_lines.append(new_line)
                modified = True
                print(f"✅ Modificada línea: {line.strip()}")
                print(f"   Nueva línea: {new_line.strip()}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    if not modified:
        print("⚠️  No se encontró línea de autenticación local para modificar")
        print("   Puede que ya esté configurada o necesites configurarla manualmente")
        return False
    
    # Escribir archivo modificado
    try:
        with open(pg_hba_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ Archivo pg_hba.conf modificado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error escribiendo pg_hba.conf: {e}")
        return False

def reiniciar_postgresql():
    """Reiniciar servicio de PostgreSQL"""
    print("🔄 Reiniciando servicio de PostgreSQL...")
    
    try:
        # Detener servicio
        result = subprocess.run([
            'net', 'stop', 'postgresql-x64-17'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servicio detenido")
        else:
            print(f"⚠️  Error deteniendo servicio: {result.stderr}")
        
        # Iniciar servicio
        result = subprocess.run([
            'net', 'start', 'postgresql-x64-17'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servicio iniciado")
            return True
        else:
            print(f"❌ Error iniciando servicio: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error reiniciando servicio: {e}")
        return False

def probar_conexion_sin_contrasena():
    """Probar conexión sin contraseña"""
    print("🔗 Probando conexión sin contraseña...")
    
    try:
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'SELECT version();'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Conexión exitosa sin contraseña")
            print(f"   Versión: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error de conexión: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False

def crear_base_datos():
    """Crear base de datos para KreaDental Cloud"""
    print("🗄️  Creando base de datos...")
    
    try:
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'CREATE DATABASE "kreadental_cloud" WITH ENCODING=\'UTF8\';'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Base de datos creada exitosamente")
            return True
        elif "already exists" in result.stderr:
            print("ℹ️  La base de datos ya existe")
            return True
        else:
            print(f"❌ Error creando base de datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def crear_env_sin_contrasena():
    """Crear archivo .env sin contraseña"""
    print("📝 Creando archivo .env sin contraseña...")
    
    env_content = """# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=
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
        print("✅ Archivo .env creado sin contraseña")
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def main():
    print("🔐 CONFIGURADOR DE POSTGRESQL SIN CONTRASEÑA")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Configurar PATH
    if not configurar_path():
        print("❌ No se pudo configurar PATH de PostgreSQL")
        return False
    
    # Configurar PostgreSQL sin contraseña
    if not configurar_postgresql_sin_contrasena():
        print("❌ No se pudo configurar PostgreSQL sin contraseña")
        return False
    
    # Reiniciar PostgreSQL
    if not reiniciar_postgresql():
        print("❌ No se pudo reiniciar PostgreSQL")
        return False
    
    # Probar conexión
    if not probar_conexion_sin_contrasena():
        print("❌ No se pudo conectar a PostgreSQL")
        return False
    
    # Crear base de datos
    if not crear_base_datos():
        print("❌ No se pudo crear la base de datos")
        return False
    
    # Crear archivo .env
    if not crear_env_sin_contrasena():
        print("❌ No se pudo crear archivo .env")
        return False
    
    print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("=" * 30)
    print("✅ PostgreSQL configurado sin contraseña")
    print("✅ Base de datos creada")
    print("✅ Archivo .env configurado")
    print("\n📝 Próximos pasos:")
    print("1. python manage.py migrate")
    print("2. python manage.py runserver")
    
    return True

if __name__ == "__main__":
    main()


"""
Script para configurar PostgreSQL sin contraseña
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

def configurar_postgresql_sin_contrasena():
    """Configurar PostgreSQL para autenticación sin contraseña"""
    print("🔧 Configurando PostgreSQL para autenticación sin contraseña...")
    
    # Ruta del archivo pg_hba.conf
    pg_hba_path = "C:\\Program Files\\PostgreSQL\\17\\data\\pg_hba.conf"
    
    if not os.path.exists(pg_hba_path):
        print(f"❌ No se encontró pg_hba.conf en: {pg_hba_path}")
        print("   Busca el archivo pg_hba.conf en tu instalación de PostgreSQL")
        return False
    
    print(f"✅ Archivo pg_hba.conf encontrado: {pg_hba_path}")
    
    # Leer archivo actual
    try:
        with open(pg_hba_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error leyendo pg_hba.conf: {e}")
        return False
    
    # Buscar línea de autenticación local
    modified = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('local') and 'all' in line and 'postgres' in line:
            # Cambiar de md5 a trust para autenticación sin contraseña
            if 'md5' in line:
                new_line = line.replace('md5', 'trust')
                new_lines.append(new_line)
                modified = True
                print(f"✅ Modificada línea: {line.strip()}")
                print(f"   Nueva línea: {new_line.strip()}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    if not modified:
        print("⚠️  No se encontró línea de autenticación local para modificar")
        print("   Puede que ya esté configurada o necesites configurarla manualmente")
        return False
    
    # Escribir archivo modificado
    try:
        with open(pg_hba_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ Archivo pg_hba.conf modificado exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error escribiendo pg_hba.conf: {e}")
        return False

def reiniciar_postgresql():
    """Reiniciar servicio de PostgreSQL"""
    print("🔄 Reiniciando servicio de PostgreSQL...")
    
    try:
        # Detener servicio
        result = subprocess.run([
            'net', 'stop', 'postgresql-x64-17'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servicio detenido")
        else:
            print(f"⚠️  Error deteniendo servicio: {result.stderr}")
        
        # Iniciar servicio
        result = subprocess.run([
            'net', 'start', 'postgresql-x64-17'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Servicio iniciado")
            return True
        else:
            print(f"❌ Error iniciando servicio: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error reiniciando servicio: {e}")
        return False

def probar_conexion_sin_contrasena():
    """Probar conexión sin contraseña"""
    print("🔗 Probando conexión sin contraseña...")
    
    try:
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'SELECT version();'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Conexión exitosa sin contraseña")
            print(f"   Versión: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error de conexión: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False

def crear_base_datos():
    """Crear base de datos para KreaDental Cloud"""
    print("🗄️  Creando base de datos...")
    
    try:
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres',
            '-c', 'CREATE DATABASE "kreadental_cloud" WITH ENCODING=\'UTF8\';'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Base de datos creada exitosamente")
            return True
        elif "already exists" in result.stderr:
            print("ℹ️  La base de datos ya existe")
            return True
        else:
            print(f"❌ Error creando base de datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def crear_env_sin_contrasena():
    """Crear archivo .env sin contraseña"""
    print("📝 Creando archivo .env sin contraseña...")
    
    env_content = """# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=
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
        print("✅ Archivo .env creado sin contraseña")
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def main():
    print("🔐 CONFIGURADOR DE POSTGRESQL SIN CONTRASEÑA")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Configurar PATH
    if not configurar_path():
        print("❌ No se pudo configurar PATH de PostgreSQL")
        return False
    
    # Configurar PostgreSQL sin contraseña
    if not configurar_postgresql_sin_contrasena():
        print("❌ No se pudo configurar PostgreSQL sin contraseña")
        return False
    
    # Reiniciar PostgreSQL
    if not reiniciar_postgresql():
        print("❌ No se pudo reiniciar PostgreSQL")
        return False
    
    # Probar conexión
    if not probar_conexion_sin_contrasena():
        print("❌ No se pudo conectar a PostgreSQL")
        return False
    
    # Crear base de datos
    if not crear_base_datos():
        print("❌ No se pudo crear la base de datos")
        return False
    
    # Crear archivo .env
    if not crear_env_sin_contrasena():
        print("❌ No se pudo crear archivo .env")
        return False
    
    print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("=" * 30)
    print("✅ PostgreSQL configurado sin contraseña")
    print("✅ Base de datos creada")
    print("✅ Archivo .env configurado")
    print("\n📝 Próximos pasos:")
    print("1. python manage.py migrate")
    print("2. python manage.py runserver")
    
    return True

if __name__ == "__main__":
    main()







