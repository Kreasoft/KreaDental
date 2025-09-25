#!/usr/bin/env python
"""
Script para verificar que la migración a PostgreSQL fue exitosa
"""

import psycopg

def verificar_migracion():
    """Verificar que la migración fue exitosa"""
    try:
        conn = psycopg.connect(
            dbname="kreadental_cloud",
            user="postgres",
            password="524302cl+",
            host="127.0.0.1",
            port="5432"
        )
        
        with conn.cursor() as cur:
            # Obtener todas las tablas
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            
            tablas = [row[0] for row in cur.fetchall()]
            
            print("📊 Verificación de migración:")
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
            
            # Verificar tablas importantes
            tablas_importantes = [
                'usuarios_usuario',
                'pacientes_paciente', 
                'profesionales_profesional',
                'empresa_empresa',
                'tratamientos_tratamiento'
            ]
            
            print("\n🔍 Verificación de tablas importantes:")
            print("-" * 40)
            
            for tabla in tablas_importantes:
                if tabla in tablas:
                    cur.execute(f'SELECT COUNT(*) FROM "{tabla}"')
                    count = cur.fetchone()[0]
                    status = "✅" if count > 0 else "⚠️"
                    print(f"   {status} {tabla}: {count} registros")
                else:
                    print(f"   ❌ {tabla}: No existe")
            
            return total_registros > 0
            
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False
    finally:
        conn.close()

def probar_aplicacion():
    """Probar que la aplicación funciona con PostgreSQL"""
    try:
        import os
        import django
        from django.core.management import execute_from_command_line
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        print("\n🧪 Probando aplicación con PostgreSQL:")
        print("-" * 40)
        
        # Probar check
        from django.core.management import call_command
        call_command('check')
        print("   ✅ Django check: OK")
        
        # Probar consulta simple
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_count = User.objects.count()
        print(f"   ✅ Usuarios en base de datos: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error probando aplicación: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Verificando migración a PostgreSQL")
    print("=" * 50)
    
    # 1. Verificar migración
    if not verificar_migracion():
        print("\n❌ La migración no fue exitosa")
        return False
    
    # 2. Probar aplicación
    if not probar_aplicacion():
        print("\n❌ La aplicación no funciona correctamente")
        return False
    
    print("\n🎉 ¡Migración completada exitosamente!")
    print("✅ KreaDental-Cloud ahora usa PostgreSQL en producción")
    return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

"""
Script para verificar que la migración a PostgreSQL fue exitosa
"""

import psycopg

def verificar_migracion():
    """Verificar que la migración fue exitosa"""
    try:
        conn = psycopg.connect(
            dbname="kreadental_cloud",
            user="postgres",
            password="524302cl+",
            host="127.0.0.1",
            port="5432"
        )
        
        with conn.cursor() as cur:
            # Obtener todas las tablas
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            
            tablas = [row[0] for row in cur.fetchall()]
            
            print("📊 Verificación de migración:")
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
            
            # Verificar tablas importantes
            tablas_importantes = [
                'usuarios_usuario',
                'pacientes_paciente', 
                'profesionales_profesional',
                'empresa_empresa',
                'tratamientos_tratamiento'
            ]
            
            print("\n🔍 Verificación de tablas importantes:")
            print("-" * 40)
            
            for tabla in tablas_importantes:
                if tabla in tablas:
                    cur.execute(f'SELECT COUNT(*) FROM "{tabla}"')
                    count = cur.fetchone()[0]
                    status = "✅" if count > 0 else "⚠️"
                    print(f"   {status} {tabla}: {count} registros")
                else:
                    print(f"   ❌ {tabla}: No existe")
            
            return total_registros > 0
            
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False
    finally:
        conn.close()

def probar_aplicacion():
    """Probar que la aplicación funciona con PostgreSQL"""
    try:
        import os
        import django
        from django.core.management import execute_from_command_line
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        print("\n🧪 Probando aplicación con PostgreSQL:")
        print("-" * 40)
        
        # Probar check
        from django.core.management import call_command
        call_command('check')
        print("   ✅ Django check: OK")
        
        # Probar consulta simple
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_count = User.objects.count()
        print(f"   ✅ Usuarios en base de datos: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error probando aplicación: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Verificando migración a PostgreSQL")
    print("=" * 50)
    
    # 1. Verificar migración
    if not verificar_migracion():
        print("\n❌ La migración no fue exitosa")
        return False
    
    # 2. Probar aplicación
    if not probar_aplicacion():
        print("\n❌ La aplicación no funciona correctamente")
        return False
    
    print("\n🎉 ¡Migración completada exitosamente!")
    print("✅ KreaDental-Cloud ahora usa PostgreSQL en producción")
    return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)










