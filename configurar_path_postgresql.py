#!/usr/bin/env python
"""
Script para configurar PATH de PostgreSQL en la sesión actual
"""

import os
import subprocess

def configurar_path_sesion():
    """Configurar PATH para la sesión actual"""
    print("🛠️  Configurando PATH de PostgreSQL para esta sesión...")
    
    # Ruta de PostgreSQL
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    
    if os.path.exists(postgresql_bin):
        print(f"✅ Ruta encontrada: {postgresql_bin}")
        
        # Agregar al PATH de la sesión actual
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
            print("✅ PATH configurado para esta sesión")
        else:
            print("✅ PATH ya contiene PostgreSQL")
        
        return True
    else:
        print(f"❌ Ruta no encontrada: {postgresql_bin}")
        return False

def verificar_psql():
    """Verificar que psql esté disponible"""
    print("🔍 Verificando psql...")
    
    try:
        result = subprocess.run(
            'psql --version',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ psql funcionando: {result.stdout.strip()}")
            return True
        else:
            print("❌ psql no responde")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando psql: {e}")
        return False

def iniciar_servicio_postgresql():
    """Intentar iniciar el servicio de PostgreSQL"""
    print("🚀 Intentando iniciar servicio de PostgreSQL...")
    
    try:
        # Iniciar servicio
        result = subprocess.run(
            'net start postgresql-x64-17',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Servicio iniciado exitosamente")
            return True
        else:
            print(f"⚠️  Error iniciando servicio: {result.stderr}")
            print("   El servicio puede estar ya ejecutándose")
            return True  # Continuar aunque haya error
            
    except Exception as e:
        print(f"❌ Error iniciando servicio: {e}")
        return False

def verificar_conexion_postgresql():
    """Verificar conexión a PostgreSQL"""
    print("🔗 Verificando conexión a PostgreSQL...")
    
    try:
        # Intentar conectar a la base de datos por defecto
        result = subprocess.run(
            'psql -U postgres -d postgres -c "SELECT version();"',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Conexión exitosa a PostgreSQL")
            print(f"   📊 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error de conexión: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando conexión: {e}")
        return False

def mostrar_instrucciones_conexion():
    """Mostrar instrucciones para conectar"""
    print("\n📋 INSTRUCCIONES DE CONEXIÓN")
    print("=" * 40)
    print("Si hay problemas de conexión:")
    print("1. Verificar que el servicio esté ejecutándose")
    print("2. Verificar la contraseña del usuario 'postgres'")
    print("3. Verificar que el puerto 5432 esté disponible")
    print("4. Intentar conectar manualmente:")
    print("   psql -U postgres -h localhost -p 5432")

def main():
    """Función principal"""
    print("🔧 CONFIGURADOR DE PATH DE POSTGRESQL")
    print("=" * 40)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 40)
    
    # Configurar PATH
    if not configurar_path_sesion():
        print("\n❌ No se pudo configurar el PATH")
        return False
    
    # Verificar psql
    if not verificar_psql():
        print("\n❌ psql no está disponible")
        return False
    
    # Iniciar servicio
    if not iniciar_servicio_postgresql():
        print("\n⚠️  No se pudo iniciar el servicio")
        print("   Continuando con la verificación...")
    
    # Verificar conexión
    if verificar_conexion_postgresql():
        print("\n🎉 PostgreSQL está funcionando correctamente")
        print("   Puedes continuar con la migración")
        return True
    else:
        print("\n⚠️  PostgreSQL no responde correctamente")
        mostrar_instrucciones_conexion()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n📝 Próximos pasos:")
        print("1. python verificar_sistema.py")
        print("2. python migrate_to_postgresql.py")
    else:
        print("\n❌ Hay problemas que resolver antes de continuar")


"""
Script para configurar PATH de PostgreSQL en la sesión actual
"""

import os
import subprocess

def configurar_path_sesion():
    """Configurar PATH para la sesión actual"""
    print("🛠️  Configurando PATH de PostgreSQL para esta sesión...")
    
    # Ruta de PostgreSQL
    postgresql_bin = "C:\\Program Files\\PostgreSQL\\17\\bin"
    
    if os.path.exists(postgresql_bin):
        print(f"✅ Ruta encontrada: {postgresql_bin}")
        
        # Agregar al PATH de la sesión actual
        current_path = os.environ.get('PATH', '')
        if postgresql_bin not in current_path:
            os.environ['PATH'] = postgresql_bin + ';' + current_path
            print("✅ PATH configurado para esta sesión")
        else:
            print("✅ PATH ya contiene PostgreSQL")
        
        return True
    else:
        print(f"❌ Ruta no encontrada: {postgresql_bin}")
        return False

def verificar_psql():
    """Verificar que psql esté disponible"""
    print("🔍 Verificando psql...")
    
    try:
        result = subprocess.run(
            'psql --version',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ psql funcionando: {result.stdout.strip()}")
            return True
        else:
            print("❌ psql no responde")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando psql: {e}")
        return False

def iniciar_servicio_postgresql():
    """Intentar iniciar el servicio de PostgreSQL"""
    print("🚀 Intentando iniciar servicio de PostgreSQL...")
    
    try:
        # Iniciar servicio
        result = subprocess.run(
            'net start postgresql-x64-17',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Servicio iniciado exitosamente")
            return True
        else:
            print(f"⚠️  Error iniciando servicio: {result.stderr}")
            print("   El servicio puede estar ya ejecutándose")
            return True  # Continuar aunque haya error
            
    except Exception as e:
        print(f"❌ Error iniciando servicio: {e}")
        return False

def verificar_conexion_postgresql():
    """Verificar conexión a PostgreSQL"""
    print("🔗 Verificando conexión a PostgreSQL...")
    
    try:
        # Intentar conectar a la base de datos por defecto
        result = subprocess.run(
            'psql -U postgres -d postgres -c "SELECT version();"',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Conexión exitosa a PostgreSQL")
            print(f"   📊 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error de conexión: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando conexión: {e}")
        return False

def mostrar_instrucciones_conexion():
    """Mostrar instrucciones para conectar"""
    print("\n📋 INSTRUCCIONES DE CONEXIÓN")
    print("=" * 40)
    print("Si hay problemas de conexión:")
    print("1. Verificar que el servicio esté ejecutándose")
    print("2. Verificar la contraseña del usuario 'postgres'")
    print("3. Verificar que el puerto 5432 esté disponible")
    print("4. Intentar conectar manualmente:")
    print("   psql -U postgres -h localhost -p 5432")

def main():
    """Función principal"""
    print("🔧 CONFIGURADOR DE PATH DE POSTGRESQL")
    print("=" * 40)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 40)
    
    # Configurar PATH
    if not configurar_path_sesion():
        print("\n❌ No se pudo configurar el PATH")
        return False
    
    # Verificar psql
    if not verificar_psql():
        print("\n❌ psql no está disponible")
        return False
    
    # Iniciar servicio
    if not iniciar_servicio_postgresql():
        print("\n⚠️  No se pudo iniciar el servicio")
        print("   Continuando con la verificación...")
    
    # Verificar conexión
    if verificar_conexion_postgresql():
        print("\n🎉 PostgreSQL está funcionando correctamente")
        print("   Puedes continuar con la migración")
        return True
    else:
        print("\n⚠️  PostgreSQL no responde correctamente")
        mostrar_instrucciones_conexion()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n📝 Próximos pasos:")
        print("1. python verificar_sistema.py")
        print("2. python migrate_to_postgresql.py")
    else:
        print("\n❌ Hay problemas que resolver antes de continuar")











