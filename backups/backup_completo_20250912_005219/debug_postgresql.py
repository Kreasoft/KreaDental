#!/usr/bin/env python
"""
Script para debuggear el problema de PostgreSQL
"""
import os
import sys
import subprocess
import psycopg2
from pathlib import Path

def probar_conexion_directa():
    """Prueba la conexión directa a PostgreSQL"""
    print("🔍 Probando conexión directa a PostgreSQL...")
    
    try:
        # Probar conexión básica
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='postgres',
            port='5432'
        )
        print("✅ Conexión básica a PostgreSQL exitosa")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en conexión básica: {e}")
        return False

def probar_conexion_base_especifica():
    """Prueba la conexión a la base de datos específica"""
    print("\n🔍 Probando conexión a base de datos específica...")
    
    try:
        # Probar conexión a kreadental_final
        conn = psycopg2.connect(
            host='localhost',
            database='kreadental_final',
            user='postgres',
            password='postgres',
            port='5432'
        )
        print("✅ Conexión a kreadental_final exitosa")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en conexión a kreadental_final: {e}")
        return False

def probar_conexion_con_encoding():
    """Prueba la conexión con diferentes encodings"""
    print("\n🔍 Probando conexión con diferentes encodings...")
    
    configuraciones = [
        {'host': 'localhost', 'database': 'kreadental_final', 'user': 'postgres', 'password': 'postgres', 'port': '5432'},
        {'host': '127.0.0.1', 'database': 'kreadental_final', 'user': 'postgres', 'password': 'postgres', 'port': '5432'},
        {'host': 'localhost', 'database': 'kreadental_final', 'user': 'postgres', 'password': 'postgres', 'port': '5432', 'client_encoding': 'UTF8'},
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

def verificar_datos_problematicos():
    """Verifica si hay datos problemáticos en el archivo de exportación"""
    print("\n🔍 Verificando datos problemáticos...")
    
    if os.path.exists('datos_exportados.json'):
        try:
            with open('datos_exportados.json', 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✅ Archivo datos_exportados.json leído correctamente ({len(content)} caracteres)")
                
                # Buscar caracteres problemáticos
                problematic_chars = []
                for i, char in enumerate(content):
                    if ord(char) > 127:  # Caracteres no ASCII
                        problematic_chars.append((i, char, ord(char)))
                        if len(problematic_chars) > 10:  # Limitar a 10 ejemplos
                            break
                
                if problematic_chars:
                    print("⚠️ Caracteres no ASCII encontrados:")
                    for pos, char, code in problematic_chars:
                        print(f"  Posición {pos}: '{char}' (código {code})")
                else:
                    print("✅ No se encontraron caracteres problemáticos")
                
                return True
        except Exception as e:
            print(f"❌ Error leyendo datos_exportados.json: {e}")
            return False
    else:
        print("❌ Archivo datos_exportados.json no encontrado")
        return False

def probar_django_con_diferentes_configs():
    """Prueba Django con diferentes configuraciones"""
    print("\n🔍 Probando Django con diferentes configuraciones...")
    
    configuraciones = [
        {
            'name': 'localhost',
            'config': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'kreadental_final',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        },
        {
            'name': '127.0.0.1',
            'config': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'kreadental_final',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': '127.0.0.1',
                'PORT': '5432',
            }
        },
        {
            'name': 'con_encoding',
            'config': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'kreadental_final',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'localhost',
                'PORT': '5432',
                'OPTIONS': {
                    'client_encoding': 'UTF8',
                },
            }
        }
    ]
    
    for config_info in configuraciones:
        print(f"\n  Probando configuración: {config_info['name']}")
        try:
            # Cambiar configuración temporalmente
            settings_file = "config/settings.py"
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Crear configuración temporal
            temp_config = f"""# Database
DATABASES = {{
    'default': {config_info['config']}
}}"""
            
            # Reemplazar configuración
            old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
            
            content = content.replace(old_config, temp_config)
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Probar comando
            result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                print(f"  ✅ Configuración {config_info['name']} exitosa")
                return True
            else:
                print(f"  ❌ Configuración {config_info['name']} falló: {result.stderr}")
                
        except Exception as e:
            print(f"  ❌ Error probando configuración {config_info['name']}: {e}")
    
    return False

def main():
    """Función principal de debug"""
    print("🚀 Iniciando debug de PostgreSQL...")
    
    # Paso 1: Probar conexión directa
    if not probar_conexion_directa():
        print("❌ No se puede conectar a PostgreSQL básico")
        return
    
    # Paso 2: Probar conexión a base específica
    if not probar_conexion_base_especifica():
        print("❌ No se puede conectar a la base de datos específica")
        return
    
    # Paso 3: Probar con diferentes encodings
    if not probar_conexion_con_encoding():
        print("❌ No se puede conectar con ningún encoding")
        return
    
    # Paso 4: Verificar datos problemáticos
    verificar_datos_problematicos()
    
    # Paso 5: Probar Django con diferentes configuraciones
    if probar_django_con_diferentes_configs():
        print("\n🎉 ¡Se encontró una configuración que funciona!")
    else:
        print("\n❌ Ninguna configuración de Django funciona")
    
    print("\n📋 Resumen del debug completado")

if __name__ == "__main__":
    main()

"""
Script para debuggear el problema de PostgreSQL
"""
import os
import sys
import subprocess
import psycopg2
from pathlib import Path

def probar_conexion_directa():
    """Prueba la conexión directa a PostgreSQL"""
    print("🔍 Probando conexión directa a PostgreSQL...")
    
    try:
        # Probar conexión básica
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='postgres',
            port='5432'
        )
        print("✅ Conexión básica a PostgreSQL exitosa")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en conexión básica: {e}")
        return False

def probar_conexion_base_especifica():
    """Prueba la conexión a la base de datos específica"""
    print("\n🔍 Probando conexión a base de datos específica...")
    
    try:
        # Probar conexión a kreadental_final
        conn = psycopg2.connect(
            host='localhost',
            database='kreadental_final',
            user='postgres',
            password='postgres',
            port='5432'
        )
        print("✅ Conexión a kreadental_final exitosa")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en conexión a kreadental_final: {e}")
        return False

def probar_conexion_con_encoding():
    """Prueba la conexión con diferentes encodings"""
    print("\n🔍 Probando conexión con diferentes encodings...")
    
    configuraciones = [
        {'host': 'localhost', 'database': 'kreadental_final', 'user': 'postgres', 'password': 'postgres', 'port': '5432'},
        {'host': '127.0.0.1', 'database': 'kreadental_final', 'user': 'postgres', 'password': 'postgres', 'port': '5432'},
        {'host': 'localhost', 'database': 'kreadental_final', 'user': 'postgres', 'password': 'postgres', 'port': '5432', 'client_encoding': 'UTF8'},
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

def verificar_datos_problematicos():
    """Verifica si hay datos problemáticos en el archivo de exportación"""
    print("\n🔍 Verificando datos problemáticos...")
    
    if os.path.exists('datos_exportados.json'):
        try:
            with open('datos_exportados.json', 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✅ Archivo datos_exportados.json leído correctamente ({len(content)} caracteres)")
                
                # Buscar caracteres problemáticos
                problematic_chars = []
                for i, char in enumerate(content):
                    if ord(char) > 127:  # Caracteres no ASCII
                        problematic_chars.append((i, char, ord(char)))
                        if len(problematic_chars) > 10:  # Limitar a 10 ejemplos
                            break
                
                if problematic_chars:
                    print("⚠️ Caracteres no ASCII encontrados:")
                    for pos, char, code in problematic_chars:
                        print(f"  Posición {pos}: '{char}' (código {code})")
                else:
                    print("✅ No se encontraron caracteres problemáticos")
                
                return True
        except Exception as e:
            print(f"❌ Error leyendo datos_exportados.json: {e}")
            return False
    else:
        print("❌ Archivo datos_exportados.json no encontrado")
        return False

def probar_django_con_diferentes_configs():
    """Prueba Django con diferentes configuraciones"""
    print("\n🔍 Probando Django con diferentes configuraciones...")
    
    configuraciones = [
        {
            'name': 'localhost',
            'config': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'kreadental_final',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        },
        {
            'name': '127.0.0.1',
            'config': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'kreadental_final',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': '127.0.0.1',
                'PORT': '5432',
            }
        },
        {
            'name': 'con_encoding',
            'config': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'kreadental_final',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'localhost',
                'PORT': '5432',
                'OPTIONS': {
                    'client_encoding': 'UTF8',
                },
            }
        }
    ]
    
    for config_info in configuraciones:
        print(f"\n  Probando configuración: {config_info['name']}")
        try:
            # Cambiar configuración temporalmente
            settings_file = "config/settings.py"
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Crear configuración temporal
            temp_config = f"""# Database
DATABASES = {{
    'default': {config_info['config']}
}}"""
            
            # Reemplazar configuración
            old_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
            
            content = content.replace(old_config, temp_config)
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Probar comando
            result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                print(f"  ✅ Configuración {config_info['name']} exitosa")
                return True
            else:
                print(f"  ❌ Configuración {config_info['name']} falló: {result.stderr}")
                
        except Exception as e:
            print(f"  ❌ Error probando configuración {config_info['name']}: {e}")
    
    return False

def main():
    """Función principal de debug"""
    print("🚀 Iniciando debug de PostgreSQL...")
    
    # Paso 1: Probar conexión directa
    if not probar_conexion_directa():
        print("❌ No se puede conectar a PostgreSQL básico")
        return
    
    # Paso 2: Probar conexión a base específica
    if not probar_conexion_base_especifica():
        print("❌ No se puede conectar a la base de datos específica")
        return
    
    # Paso 3: Probar con diferentes encodings
    if not probar_conexion_con_encoding():
        print("❌ No se puede conectar con ningún encoding")
        return
    
    # Paso 4: Verificar datos problemáticos
    verificar_datos_problematicos()
    
    # Paso 5: Probar Django con diferentes configuraciones
    if probar_django_con_diferentes_configs():
        print("\n🎉 ¡Se encontró una configuración que funciona!")
    else:
        print("\n❌ Ninguna configuración de Django funciona")
    
    print("\n📋 Resumen del debug completado")

if __name__ == "__main__":
    main()




