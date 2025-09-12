#!/usr/bin/env python
"""
Script para configurar PostgreSQL en Windows
"""

import os
import subprocess
import glob
from pathlib import Path

def buscar_postgresql():
    """Buscar instalación de PostgreSQL"""
    print("🔍 Buscando instalación de PostgreSQL...")
    
    ubicaciones = [
        "C:\\Program Files\\PostgreSQL",
        "C:\\Program Files (x86)\\PostgreSQL",
        "C:\\PostgreSQL"
    ]
    
    for ubicacion in ubicaciones:
        if os.path.exists(ubicacion):
            print(f"✅ PostgreSQL encontrado en: {ubicacion}")
            
            # Buscar subdirectorios con versiones
            subdirs = [d for d in os.listdir(ubicacion) if os.path.isdir(os.path.join(ubicacion, d))]
            for subdir in subdirs:
                bin_path = os.path.join(ubicacion, subdir, "bin")
                if os.path.exists(bin_path):
                    print(f"   📁 Versión: {subdir}")
                    print(f"   📁 Binarios: {bin_path}")
                    return bin_path
    
    print("❌ No se encontró instalación de PostgreSQL")
    return None

def verificar_psql(bin_path):
    """Verificar que psql esté disponible"""
    print("🔍 Verificando psql...")
    
    psql_path = os.path.join(bin_path, "psql.exe")
    if os.path.exists(psql_path):
        print(f"✅ psql encontrado: {psql_path}")
        return psql_path
    else:
        print(f"❌ psql no encontrado en: {psql_path}")
        return None

def verificar_servicio_postgresql():
    """Verificar servicios de PostgreSQL"""
    print("🔍 Verificando servicios de PostgreSQL...")
    
    try:
        # Buscar servicios que contengan 'postgres'
        result = subprocess.run(
            'sc query | findstr -i postgres',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Servicios de PostgreSQL encontrados:")
            print(result.stdout)
            return True
        else:
            print("❌ No se encontraron servicios de PostgreSQL")
            return False
            
    except Exception as e:
        print(f"❌ Error buscando servicios: {e}")
        return False

def iniciar_postgresql_manual(bin_path):
    """Intentar iniciar PostgreSQL manualmente"""
    print("🚀 Intentando iniciar PostgreSQL manualmente...")
    
    try:
        # Buscar pg_ctl
        pg_ctl_path = os.path.join(bin_path, "pg_ctl.exe")
        if os.path.exists(pg_ctl_path):
            print(f"✅ pg_ctl encontrado: {pg_ctl_path}")
            
            # Intentar iniciar
            result = subprocess.run(
                f'"{pg_ctl_path}" start -D "C:\\Program Files\\PostgreSQL\\14\\data"',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ PostgreSQL iniciado manualmente")
                return True
            else:
                print(f"❌ Error iniciando PostgreSQL: {result.stderr}")
                return False
        else:
            print("❌ pg_ctl no encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando PostgreSQL: {e}")
        return False

def configurar_path(bin_path):
    """Configurar PATH para PostgreSQL"""
    print("🛠️  Configurando PATH para PostgreSQL...")
    
    print(f"📁 Ruta a agregar: {bin_path}")
    print("\n📋 INSTRUCCIONES MANUALES:")
    print("=" * 40)
    print("1. Abrir 'Variables de entorno del sistema'")
    print("2. En 'Variables del sistema', buscar 'Path'")
    print("3. Hacer clic en 'Editar'")
    print("4. Hacer clic en 'Nuevo'")
    print(f"5. Agregar: {bin_path}")
    print("6. Hacer clic en 'Aceptar' en todas las ventanas")
    print("7. Reiniciar la terminal/consola")
    print("8. Verificar con: psql --version")

def verificar_conexion():
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

def mostrar_instrucciones_instalacion():
    """Mostrar instrucciones de instalación"""
    print("\n📥 INSTRUCCIONES DE INSTALACIÓN")
    print("=" * 40)
    print("1. Descargar PostgreSQL desde:")
    print("   https://www.postgresql.org/download/windows/")
    print("2. Ejecutar el instalador como administrador")
    print("3. Durante la instalación:")
    print("   - Recordar la contraseña del usuario 'postgres'")
    print("   - Anotar el puerto (por defecto 5432)")
    print("   - Asegurar que se instale pgAdmin")
    print("4. Al finalizar, reiniciar el sistema")
    print("5. Verificar la instalación")

def main():
    """Función principal"""
    print("🐘 CONFIGURADOR DE POSTGRESQL PARA WINDOWS")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Buscar PostgreSQL
    bin_path = buscar_postgresql()
    
    if not bin_path:
        print("\n❌ PostgreSQL no está instalado")
        mostrar_instrucciones_instalacion()
        return False
    
    # Verificar psql
    psql_path = verificar_psql(bin_path)
    if not psql_path:
        print("\n❌ psql no está disponible")
        return False
    
    # Verificar servicios
    if not verificar_servicio_postgresql():
        print("\n⚠️  No se encontraron servicios de PostgreSQL")
        print("   Esto puede ser normal si PostgreSQL no se instaló como servicio")
    
    # Verificar conexión
    if verificar_conexion():
        print("\n🎉 PostgreSQL está funcionando correctamente")
        return True
    else:
        print("\n⚠️  PostgreSQL no responde")
        print("   Configurando PATH...")
        configurar_path(bin_path)
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n📝 Próximos pasos:")
        print("1. python verificar_sistema.py")
        print("2. python migrate_to_postgresql.py")
    else:
        print("\n❌ Hay problemas que resolver antes de continuar")
        print("   Sigue las instrucciones mostradas arriba")


"""
Script para configurar PostgreSQL en Windows
"""

import os
import subprocess
import glob
from pathlib import Path

def buscar_postgresql():
    """Buscar instalación de PostgreSQL"""
    print("🔍 Buscando instalación de PostgreSQL...")
    
    ubicaciones = [
        "C:\\Program Files\\PostgreSQL",
        "C:\\Program Files (x86)\\PostgreSQL",
        "C:\\PostgreSQL"
    ]
    
    for ubicacion in ubicaciones:
        if os.path.exists(ubicacion):
            print(f"✅ PostgreSQL encontrado en: {ubicacion}")
            
            # Buscar subdirectorios con versiones
            subdirs = [d for d in os.listdir(ubicacion) if os.path.isdir(os.path.join(ubicacion, d))]
            for subdir in subdirs:
                bin_path = os.path.join(ubicacion, subdir, "bin")
                if os.path.exists(bin_path):
                    print(f"   📁 Versión: {subdir}")
                    print(f"   📁 Binarios: {bin_path}")
                    return bin_path
    
    print("❌ No se encontró instalación de PostgreSQL")
    return None

def verificar_psql(bin_path):
    """Verificar que psql esté disponible"""
    print("🔍 Verificando psql...")
    
    psql_path = os.path.join(bin_path, "psql.exe")
    if os.path.exists(psql_path):
        print(f"✅ psql encontrado: {psql_path}")
        return psql_path
    else:
        print(f"❌ psql no encontrado en: {psql_path}")
        return None

def verificar_servicio_postgresql():
    """Verificar servicios de PostgreSQL"""
    print("🔍 Verificando servicios de PostgreSQL...")
    
    try:
        # Buscar servicios que contengan 'postgres'
        result = subprocess.run(
            'sc query | findstr -i postgres',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Servicios de PostgreSQL encontrados:")
            print(result.stdout)
            return True
        else:
            print("❌ No se encontraron servicios de PostgreSQL")
            return False
            
    except Exception as e:
        print(f"❌ Error buscando servicios: {e}")
        return False

def iniciar_postgresql_manual(bin_path):
    """Intentar iniciar PostgreSQL manualmente"""
    print("🚀 Intentando iniciar PostgreSQL manualmente...")
    
    try:
        # Buscar pg_ctl
        pg_ctl_path = os.path.join(bin_path, "pg_ctl.exe")
        if os.path.exists(pg_ctl_path):
            print(f"✅ pg_ctl encontrado: {pg_ctl_path}")
            
            # Intentar iniciar
            result = subprocess.run(
                f'"{pg_ctl_path}" start -D "C:\\Program Files\\PostgreSQL\\14\\data"',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ PostgreSQL iniciado manualmente")
                return True
            else:
                print(f"❌ Error iniciando PostgreSQL: {result.stderr}")
                return False
        else:
            print("❌ pg_ctl no encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando PostgreSQL: {e}")
        return False

def configurar_path(bin_path):
    """Configurar PATH para PostgreSQL"""
    print("🛠️  Configurando PATH para PostgreSQL...")
    
    print(f"📁 Ruta a agregar: {bin_path}")
    print("\n📋 INSTRUCCIONES MANUALES:")
    print("=" * 40)
    print("1. Abrir 'Variables de entorno del sistema'")
    print("2. En 'Variables del sistema', buscar 'Path'")
    print("3. Hacer clic en 'Editar'")
    print("4. Hacer clic en 'Nuevo'")
    print(f"5. Agregar: {bin_path}")
    print("6. Hacer clic en 'Aceptar' en todas las ventanas")
    print("7. Reiniciar la terminal/consola")
    print("8. Verificar con: psql --version")

def verificar_conexion():
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

def mostrar_instrucciones_instalacion():
    """Mostrar instrucciones de instalación"""
    print("\n📥 INSTRUCCIONES DE INSTALACIÓN")
    print("=" * 40)
    print("1. Descargar PostgreSQL desde:")
    print("   https://www.postgresql.org/download/windows/")
    print("2. Ejecutar el instalador como administrador")
    print("3. Durante la instalación:")
    print("   - Recordar la contraseña del usuario 'postgres'")
    print("   - Anotar el puerto (por defecto 5432)")
    print("   - Asegurar que se instale pgAdmin")
    print("4. Al finalizar, reiniciar el sistema")
    print("5. Verificar la instalación")

def main():
    """Función principal"""
    print("🐘 CONFIGURADOR DE POSTGRESQL PARA WINDOWS")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Buscar PostgreSQL
    bin_path = buscar_postgresql()
    
    if not bin_path:
        print("\n❌ PostgreSQL no está instalado")
        mostrar_instrucciones_instalacion()
        return False
    
    # Verificar psql
    psql_path = verificar_psql(bin_path)
    if not psql_path:
        print("\n❌ psql no está disponible")
        return False
    
    # Verificar servicios
    if not verificar_servicio_postgresql():
        print("\n⚠️  No se encontraron servicios de PostgreSQL")
        print("   Esto puede ser normal si PostgreSQL no se instaló como servicio")
    
    # Verificar conexión
    if verificar_conexion():
        print("\n🎉 PostgreSQL está funcionando correctamente")
        return True
    else:
        print("\n⚠️  PostgreSQL no responde")
        print("   Configurando PATH...")
        configurar_path(bin_path)
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n📝 Próximos pasos:")
        print("1. python verificar_sistema.py")
        print("2. python migrate_to_postgresql.py")
    else:
        print("\n❌ Hay problemas que resolver antes de continuar")
        print("   Sigue las instrucciones mostradas arriba")





