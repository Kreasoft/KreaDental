#!/usr/bin/env python
"""
Script interactivo para configurar PostgreSQL
"""

import os
import getpass

def crear_archivo_env():
    """Crear archivo .env interactivamente"""
    
    print("🔧 Configuración de PostgreSQL para KreaDental Cloud")
    print("=" * 50)
    
    # Valores por defecto
    config = {
        'DB_NAME': 'kreadental_cloud',
        'DB_USER': 'postgres',
        'DB_PASSWORD': '',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'SECRET_KEY': 'django-insecure-your-secret-key-here',
        'DEBUG': 'True',
        'ALLOWED_HOSTS': 'localhost,127.0.0.1'
    }
    
    print("\n📝 Configuración de la base de datos:")
    print("(Presiona Enter para usar valores por defecto)")
    
    # Solicitar configuración
    config['DB_NAME'] = input(f"Nombre de la base de datos [{config['DB_NAME']}]: ") or config['DB_NAME']
    config['DB_USER'] = input(f"Usuario de PostgreSQL [{config['DB_USER']}]: ") or config['DB_USER']
    config['DB_PASSWORD'] = getpass.getpass("Contraseña de PostgreSQL: ")
    config['DB_HOST'] = input(f"Host de PostgreSQL [{config['DB_HOST']}]: ") or config['DB_HOST']
    config['DB_PORT'] = input(f"Puerto de PostgreSQL [{config['DB_PORT']}]: ") or config['DB_PORT']
    
    print("\n🔐 Configuración de Django:")
    config['SECRET_KEY'] = input(f"Secret Key de Django [{config['SECRET_KEY']}]: ") or config['SECRET_KEY']
    
    # Crear archivo .env
    env_content = f"""# Configuración de PostgreSQL
DB_NAME={config['DB_NAME']}
DB_USER={config['DB_USER']}
DB_PASSWORD={config['DB_PASSWORD']}
DB_HOST={config['DB_HOST']}
DB_PORT={config['DB_PORT']}

# Configuración de Django
SECRET_KEY={config['SECRET_KEY']}
DEBUG={config['DEBUG']}
ALLOWED_HOSTS={config['ALLOWED_HOSTS']}
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n✅ Archivo .env creado exitosamente")
        print("📁 Ubicación: .env")
        
        # Mostrar resumen
        print("\n📋 Resumen de configuración:")
        print("-" * 30)
        for key, value in config.items():
            if key == 'DB_PASSWORD':
                print(f"   {key}: {'*' * len(value)}")
            else:
                print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creando archivo .env: {e}")
        return False

def verificar_conexion():
    """Verificar conexión a PostgreSQL"""
    print("\n🔍 Verificando conexión a PostgreSQL...")
    
    try:
        import psycopg2
        from dotenv import load_dotenv
        
        load_dotenv()
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': 'postgres'  # Conectar a la base de datos por defecto
        }
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Conexión exitosa a PostgreSQL")
        print(f"   📊 Versión: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n💡 Posibles soluciones:")
        print("   - Verificar que PostgreSQL esté ejecutándose")
        print("   - Verificar las credenciales")
        print("   - Verificar que el puerto esté disponible")
        return False

def main():
    """Función principal"""
    print("🚀 Configurador de PostgreSQL para KreaDental Cloud")
    print("=" * 60)
    
    # Crear archivo .env
    if crear_archivo_env():
        # Verificar conexión
        if verificar_conexion():
            print("\n🎉 Configuración completada exitosamente!")
            print("\n📝 Próximos pasos:")
            print("   1. Ejecutar: python config_database.py")
            print("   2. Ejecutar: python migrate_to_postgresql.py")
            print("   3. Ejecutar: python manage.py runserver")
        else:
            print("\n⚠️  Configuración guardada, pero hay problemas de conexión")
            print("   Revisa la configuración y vuelve a intentar")
    else:
        print("\n❌ Error en la configuración")

if __name__ == "__main__":
    main()


"""
Script interactivo para configurar PostgreSQL
"""

import os
import getpass

def crear_archivo_env():
    """Crear archivo .env interactivamente"""
    
    print("🔧 Configuración de PostgreSQL para KreaDental Cloud")
    print("=" * 50)
    
    # Valores por defecto
    config = {
        'DB_NAME': 'kreadental_cloud',
        'DB_USER': 'postgres',
        'DB_PASSWORD': '',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'SECRET_KEY': 'django-insecure-your-secret-key-here',
        'DEBUG': 'True',
        'ALLOWED_HOSTS': 'localhost,127.0.0.1'
    }
    
    print("\n📝 Configuración de la base de datos:")
    print("(Presiona Enter para usar valores por defecto)")
    
    # Solicitar configuración
    config['DB_NAME'] = input(f"Nombre de la base de datos [{config['DB_NAME']}]: ") or config['DB_NAME']
    config['DB_USER'] = input(f"Usuario de PostgreSQL [{config['DB_USER']}]: ") or config['DB_USER']
    config['DB_PASSWORD'] = getpass.getpass("Contraseña de PostgreSQL: ")
    config['DB_HOST'] = input(f"Host de PostgreSQL [{config['DB_HOST']}]: ") or config['DB_HOST']
    config['DB_PORT'] = input(f"Puerto de PostgreSQL [{config['DB_PORT']}]: ") or config['DB_PORT']
    
    print("\n🔐 Configuración de Django:")
    config['SECRET_KEY'] = input(f"Secret Key de Django [{config['SECRET_KEY']}]: ") or config['SECRET_KEY']
    
    # Crear archivo .env
    env_content = f"""# Configuración de PostgreSQL
DB_NAME={config['DB_NAME']}
DB_USER={config['DB_USER']}
DB_PASSWORD={config['DB_PASSWORD']}
DB_HOST={config['DB_HOST']}
DB_PORT={config['DB_PORT']}

# Configuración de Django
SECRET_KEY={config['SECRET_KEY']}
DEBUG={config['DEBUG']}
ALLOWED_HOSTS={config['ALLOWED_HOSTS']}
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n✅ Archivo .env creado exitosamente")
        print("📁 Ubicación: .env")
        
        # Mostrar resumen
        print("\n📋 Resumen de configuración:")
        print("-" * 30)
        for key, value in config.items():
            if key == 'DB_PASSWORD':
                print(f"   {key}: {'*' * len(value)}")
            else:
                print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creando archivo .env: {e}")
        return False

def verificar_conexion():
    """Verificar conexión a PostgreSQL"""
    print("\n🔍 Verificando conexión a PostgreSQL...")
    
    try:
        import psycopg2
        from dotenv import load_dotenv
        
        load_dotenv()
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': 'postgres'  # Conectar a la base de datos por defecto
        }
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Conexión exitosa a PostgreSQL")
        print(f"   📊 Versión: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n💡 Posibles soluciones:")
        print("   - Verificar que PostgreSQL esté ejecutándose")
        print("   - Verificar las credenciales")
        print("   - Verificar que el puerto esté disponible")
        return False

def main():
    """Función principal"""
    print("🚀 Configurador de PostgreSQL para KreaDental Cloud")
    print("=" * 60)
    
    # Crear archivo .env
    if crear_archivo_env():
        # Verificar conexión
        if verificar_conexion():
            print("\n🎉 Configuración completada exitosamente!")
            print("\n📝 Próximos pasos:")
            print("   1. Ejecutar: python config_database.py")
            print("   2. Ejecutar: python migrate_to_postgresql.py")
            print("   3. Ejecutar: python manage.py runserver")
        else:
            print("\n⚠️  Configuración guardada, pero hay problemas de conexión")
            print("   Revisa la configuración y vuelve a intentar")
    else:
        print("\n❌ Error en la configuración")

if __name__ == "__main__":
    main()





