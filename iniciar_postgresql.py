#!/usr/bin/env python
"""
Script para iniciar el servicio de PostgreSQL en Windows
"""

import subprocess
import os
import time

def encontrar_servicio_postgresql():
    """Encontrar el nombre del servicio de PostgreSQL"""
    print("🔍 Buscando servicio de PostgreSQL...")
    
    try:
        # Listar servicios que contengan 'postgres'
        result = subprocess.run(
            'sc query | findstr postgres',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'SERVICE_NAME' in line:
                    service_name = line.split(':')[1].strip()
                    print(f"✅ Servicio encontrado: {service_name}")
                    return service_name
        
        print("❌ No se encontró servicio de PostgreSQL")
        return None
        
    except Exception as e:
        print(f"❌ Error buscando servicio: {e}")
        return None

def iniciar_servicio(service_name):
    """Iniciar el servicio de PostgreSQL"""
    print(f"🚀 Iniciando servicio: {service_name}")
    
    try:
        # Iniciar servicio
        result = subprocess.run(
            f'net start "{service_name}"',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Servicio iniciado exitosamente")
            return True
        else:
            print(f"❌ Error iniciando servicio: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando servicio: {e}")
        return False

def verificar_servicio_activo(service_name):
    """Verificar que el servicio esté activo"""
    print("🔍 Verificando estado del servicio...")
    
    try:
        result = subprocess.run(
            f'sc query "{service_name}"',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if "RUNNING" in result.stdout:
            print("✅ Servicio está ejecutándose")
            return True
        else:
            print("⚠️  Servicio no está ejecutándose")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando servicio: {e}")
        return False

def verificar_conexion_postgresql():
    """Verificar conexión a PostgreSQL"""
    print("🔗 Verificando conexión a PostgreSQL...")
    
    try:
        result = subprocess.run(
            'psql --version',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ PostgreSQL funcionando: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL no responde")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando PostgreSQL: {e}")
        return False

def configurar_path_postgresql():
    """Mostrar cómo configurar el PATH"""
    print("\n🛠️  CONFIGURACIÓN DEL PATH")
    print("=" * 30)
    print("Si psql no se encuentra, agrega al PATH:")
    print("C:\\Program Files\\PostgreSQL\\14\\bin")
    print("(o la versión que tengas instalada)")
    print("\nPasos:")
    print("1. Abrir 'Variables de entorno del sistema'")
    print("2. En 'Variables del sistema', buscar 'Path'")
    print("3. Agregar la ruta del binario")
    print("4. Reiniciar la terminal")

def main():
    """Función principal"""
    print("🚀 INICIADOR DE POSTGRESQL")
    print("=" * 30)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 30)
    
    # Buscar servicio
    service_name = encontrar_servicio_postgresql()
    
    if not service_name:
        print("\n❌ No se encontró servicio de PostgreSQL")
        print("   Verifica que PostgreSQL esté instalado correctamente")
        return False
    
    # Verificar si ya está ejecutándose
    if verificar_servicio_activo(service_name):
        print("\n✅ El servicio ya está ejecutándose")
    else:
        # Iniciar servicio
        if iniciar_servicio(service_name):
            print("\n⏳ Esperando que el servicio se inicie...")
            time.sleep(3)
            
            # Verificar que esté activo
            if verificar_servicio_activo(service_name):
                print("✅ Servicio iniciado correctamente")
            else:
                print("❌ El servicio no se inició correctamente")
                return False
        else:
            print("\n❌ No se pudo iniciar el servicio")
            print("   Intenta iniciarlo manualmente desde 'Servicios de Windows'")
            return False
    
    # Verificar conexión
    if verificar_conexion_postgresql():
        print("\n🎉 PostgreSQL está listo para usar")
        print("   Puedes continuar con la migración")
        return True
    else:
        print("\n⚠️  El servicio está ejecutándose pero psql no responde")
        configurar_path_postgresql()
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
Script para iniciar el servicio de PostgreSQL en Windows
"""

import subprocess
import os
import time

def encontrar_servicio_postgresql():
    """Encontrar el nombre del servicio de PostgreSQL"""
    print("🔍 Buscando servicio de PostgreSQL...")
    
    try:
        # Listar servicios que contengan 'postgres'
        result = subprocess.run(
            'sc query | findstr postgres',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'SERVICE_NAME' in line:
                    service_name = line.split(':')[1].strip()
                    print(f"✅ Servicio encontrado: {service_name}")
                    return service_name
        
        print("❌ No se encontró servicio de PostgreSQL")
        return None
        
    except Exception as e:
        print(f"❌ Error buscando servicio: {e}")
        return None

def iniciar_servicio(service_name):
    """Iniciar el servicio de PostgreSQL"""
    print(f"🚀 Iniciando servicio: {service_name}")
    
    try:
        # Iniciar servicio
        result = subprocess.run(
            f'net start "{service_name}"',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Servicio iniciado exitosamente")
            return True
        else:
            print(f"❌ Error iniciando servicio: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando servicio: {e}")
        return False

def verificar_servicio_activo(service_name):
    """Verificar que el servicio esté activo"""
    print("🔍 Verificando estado del servicio...")
    
    try:
        result = subprocess.run(
            f'sc query "{service_name}"',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if "RUNNING" in result.stdout:
            print("✅ Servicio está ejecutándose")
            return True
        else:
            print("⚠️  Servicio no está ejecutándose")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando servicio: {e}")
        return False

def verificar_conexion_postgresql():
    """Verificar conexión a PostgreSQL"""
    print("🔗 Verificando conexión a PostgreSQL...")
    
    try:
        result = subprocess.run(
            'psql --version',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ PostgreSQL funcionando: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL no responde")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando PostgreSQL: {e}")
        return False

def configurar_path_postgresql():
    """Mostrar cómo configurar el PATH"""
    print("\n🛠️  CONFIGURACIÓN DEL PATH")
    print("=" * 30)
    print("Si psql no se encuentra, agrega al PATH:")
    print("C:\\Program Files\\PostgreSQL\\14\\bin")
    print("(o la versión que tengas instalada)")
    print("\nPasos:")
    print("1. Abrir 'Variables de entorno del sistema'")
    print("2. En 'Variables del sistema', buscar 'Path'")
    print("3. Agregar la ruta del binario")
    print("4. Reiniciar la terminal")

def main():
    """Función principal"""
    print("🚀 INICIADOR DE POSTGRESQL")
    print("=" * 30)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 30)
    
    # Buscar servicio
    service_name = encontrar_servicio_postgresql()
    
    if not service_name:
        print("\n❌ No se encontró servicio de PostgreSQL")
        print("   Verifica que PostgreSQL esté instalado correctamente")
        return False
    
    # Verificar si ya está ejecutándose
    if verificar_servicio_activo(service_name):
        print("\n✅ El servicio ya está ejecutándose")
    else:
        # Iniciar servicio
        if iniciar_servicio(service_name):
            print("\n⏳ Esperando que el servicio se inicie...")
            time.sleep(3)
            
            # Verificar que esté activo
            if verificar_servicio_activo(service_name):
                print("✅ Servicio iniciado correctamente")
            else:
                print("❌ El servicio no se inició correctamente")
                return False
        else:
            print("\n❌ No se pudo iniciar el servicio")
            print("   Intenta iniciarlo manualmente desde 'Servicios de Windows'")
            return False
    
    # Verificar conexión
    if verificar_conexion_postgresql():
        print("\n🎉 PostgreSQL está listo para usar")
        print("   Puedes continuar con la migración")
        return True
    else:
        print("\n⚠️  El servicio está ejecutándose pero psql no responde")
        configurar_path_postgresql()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n📝 Próximos pasos:")
        print("1. python verificar_sistema.py")
        print("2. python migrate_to_postgresql.py")
    else:
        print("\n❌ Hay problemas que resolver antes de continuar")





