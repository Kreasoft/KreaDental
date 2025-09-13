#!/usr/bin/env python
"""
Script para ayudar con la instalación de PostgreSQL en Windows
"""

import os
import subprocess
import webbrowser
from pathlib import Path

def verificar_postgresql_instalado():
    """Verificar si PostgreSQL ya está instalado"""
    print("🔍 Verificando si PostgreSQL está instalado...")
    
    # Verificar en el PATH
    try:
        result = subprocess.run("psql --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL encontrado: {result.stdout.strip()}")
            return True
    except:
        pass
    
    # Verificar en ubicaciones comunes de Windows
    ubicaciones_comunes = [
        "C:\\Program Files\\PostgreSQL",
        "C:\\Program Files (x86)\\PostgreSQL",
        "C:\\PostgreSQL"
    ]
    
    for ubicacion in ubicaciones_comunes:
        if os.path.exists(ubicacion):
            print(f"✅ PostgreSQL encontrado en: {ubicacion}")
            return True
    
    print("❌ PostgreSQL no está instalado")
    return False

def descargar_postgresql():
    """Abrir página de descarga de PostgreSQL"""
    print("🌐 Abriendo página de descarga de PostgreSQL...")
    
    url = "https://www.postgresql.org/download/windows/"
    print(f"📥 URL de descarga: {url}")
    
    try:
        webbrowser.open(url)
        print("✅ Página de descarga abierta en el navegador")
        return True
    except Exception as e:
        print(f"❌ Error abriendo navegador: {e}")
        return False

def mostrar_instrucciones_instalacion():
    """Mostrar instrucciones de instalación"""
    print("\n📋 INSTRUCCIONES DE INSTALACIÓN")
    print("=" * 50)
    print("1. Descargar PostgreSQL desde la página que se abrió")
    print("2. Ejecutar el instalador como administrador")
    print("3. Durante la instalación:")
    print("   - Recordar la contraseña del usuario 'postgres'")
    print("   - Anotar el puerto (por defecto 5432)")
    print("   - Asegurar que se instale pgAdmin (opcional pero útil)")
    print("4. Al finalizar, reiniciar el sistema")
    print("5. Verificar la instalación ejecutando:")
    print("   psql --version")
    print("\n💡 CONSEJOS:")
    print("- Usa una contraseña segura pero fácil de recordar")
    print("- El puerto 5432 es el estándar, no lo cambies a menos que sea necesario")
    print("- pgAdmin es una herramienta gráfica útil para administrar PostgreSQL")

def verificar_servicio_postgresql():
    """Verificar si el servicio de PostgreSQL está ejecutándose"""
    print("\n🔧 Verificando servicio de PostgreSQL...")
    
    try:
        # Verificar servicio usando sc
        result = subprocess.run(
            'sc query postgresql-x64-14', 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if "RUNNING" in result.stdout:
            print("✅ Servicio PostgreSQL está ejecutándose")
            return True
        else:
            print("⚠️  Servicio PostgreSQL no está ejecutándose")
            print("   Intenta iniciarlo desde Servicios de Windows")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando servicio: {e}")
        return False

def configurar_path_postgresql():
    """Mostrar cómo configurar el PATH para PostgreSQL"""
    print("\n🛠️  CONFIGURACIÓN DEL PATH")
    print("=" * 30)
    print("Si PostgreSQL no se encuentra en el PATH:")
    print("1. Abrir 'Variables de entorno del sistema'")
    print("2. En 'Variables del sistema', buscar 'Path'")
    print("3. Agregar la ruta del binario de PostgreSQL:")
    print("   C:\\Program Files\\PostgreSQL\\14\\bin")
    print("4. Reiniciar la terminal/consola")
    print("5. Verificar con: psql --version")

def main():
    """Función principal"""
    print("🐘 INSTALADOR DE POSTGRESQL PARA WINDOWS")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Verificar si ya está instalado
    if verificar_postgresql_instalado():
        print("\n✅ PostgreSQL ya está instalado")
        
        # Verificar servicio
        if verificar_servicio_postgresql():
            print("\n🎉 PostgreSQL está listo para usar")
            print("   Puedes continuar con la migración")
        else:
            print("\n⚠️  PostgreSQL está instalado pero el servicio no está ejecutándose")
            print("   Inicia el servicio desde 'Servicios de Windows'")
    else:
        print("\n📥 PostgreSQL no está instalado")
        print("   Procediendo con la descarga...")
        
        # Descargar PostgreSQL
        if descargar_postgresql():
            mostrar_instrucciones_instalacion()
        else:
            print("\n❌ No se pudo abrir la página de descarga")
            print("   Visita manualmente: https://www.postgresql.org/download/windows/")
    
    print("\n" + "=" * 50)
    print("📝 PRÓXIMOS PASOS DESPUÉS DE INSTALAR")
    print("=" * 50)
    print("1. Verificar instalación: psql --version")
    print("2. Configurar .env: python configurar_postgresql.py")
    print("3. Verificar sistema: python verificar_sistema.py")
    print("4. Migrar a PostgreSQL: python migrate_to_postgresql.py")

if __name__ == "__main__":
    main()


"""
Script para ayudar con la instalación de PostgreSQL en Windows
"""

import os
import subprocess
import webbrowser
from pathlib import Path

def verificar_postgresql_instalado():
    """Verificar si PostgreSQL ya está instalado"""
    print("🔍 Verificando si PostgreSQL está instalado...")
    
    # Verificar en el PATH
    try:
        result = subprocess.run("psql --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL encontrado: {result.stdout.strip()}")
            return True
    except:
        pass
    
    # Verificar en ubicaciones comunes de Windows
    ubicaciones_comunes = [
        "C:\\Program Files\\PostgreSQL",
        "C:\\Program Files (x86)\\PostgreSQL",
        "C:\\PostgreSQL"
    ]
    
    for ubicacion in ubicaciones_comunes:
        if os.path.exists(ubicacion):
            print(f"✅ PostgreSQL encontrado en: {ubicacion}")
            return True
    
    print("❌ PostgreSQL no está instalado")
    return False

def descargar_postgresql():
    """Abrir página de descarga de PostgreSQL"""
    print("🌐 Abriendo página de descarga de PostgreSQL...")
    
    url = "https://www.postgresql.org/download/windows/"
    print(f"📥 URL de descarga: {url}")
    
    try:
        webbrowser.open(url)
        print("✅ Página de descarga abierta en el navegador")
        return True
    except Exception as e:
        print(f"❌ Error abriendo navegador: {e}")
        return False

def mostrar_instrucciones_instalacion():
    """Mostrar instrucciones de instalación"""
    print("\n📋 INSTRUCCIONES DE INSTALACIÓN")
    print("=" * 50)
    print("1. Descargar PostgreSQL desde la página que se abrió")
    print("2. Ejecutar el instalador como administrador")
    print("3. Durante la instalación:")
    print("   - Recordar la contraseña del usuario 'postgres'")
    print("   - Anotar el puerto (por defecto 5432)")
    print("   - Asegurar que se instale pgAdmin (opcional pero útil)")
    print("4. Al finalizar, reiniciar el sistema")
    print("5. Verificar la instalación ejecutando:")
    print("   psql --version")
    print("\n💡 CONSEJOS:")
    print("- Usa una contraseña segura pero fácil de recordar")
    print("- El puerto 5432 es el estándar, no lo cambies a menos que sea necesario")
    print("- pgAdmin es una herramienta gráfica útil para administrar PostgreSQL")

def verificar_servicio_postgresql():
    """Verificar si el servicio de PostgreSQL está ejecutándose"""
    print("\n🔧 Verificando servicio de PostgreSQL...")
    
    try:
        # Verificar servicio usando sc
        result = subprocess.run(
            'sc query postgresql-x64-14', 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if "RUNNING" in result.stdout:
            print("✅ Servicio PostgreSQL está ejecutándose")
            return True
        else:
            print("⚠️  Servicio PostgreSQL no está ejecutándose")
            print("   Intenta iniciarlo desde Servicios de Windows")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando servicio: {e}")
        return False

def configurar_path_postgresql():
    """Mostrar cómo configurar el PATH para PostgreSQL"""
    print("\n🛠️  CONFIGURACIÓN DEL PATH")
    print("=" * 30)
    print("Si PostgreSQL no se encuentra en el PATH:")
    print("1. Abrir 'Variables de entorno del sistema'")
    print("2. En 'Variables del sistema', buscar 'Path'")
    print("3. Agregar la ruta del binario de PostgreSQL:")
    print("   C:\\Program Files\\PostgreSQL\\14\\bin")
    print("4. Reiniciar la terminal/consola")
    print("5. Verificar con: psql --version")

def main():
    """Función principal"""
    print("🐘 INSTALADOR DE POSTGRESQL PARA WINDOWS")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Verificar si ya está instalado
    if verificar_postgresql_instalado():
        print("\n✅ PostgreSQL ya está instalado")
        
        # Verificar servicio
        if verificar_servicio_postgresql():
            print("\n🎉 PostgreSQL está listo para usar")
            print("   Puedes continuar con la migración")
        else:
            print("\n⚠️  PostgreSQL está instalado pero el servicio no está ejecutándose")
            print("   Inicia el servicio desde 'Servicios de Windows'")
    else:
        print("\n📥 PostgreSQL no está instalado")
        print("   Procediendo con la descarga...")
        
        # Descargar PostgreSQL
        if descargar_postgresql():
            mostrar_instrucciones_instalacion()
        else:
            print("\n❌ No se pudo abrir la página de descarga")
            print("   Visita manualmente: https://www.postgresql.org/download/windows/")
    
    print("\n" + "=" * 50)
    print("📝 PRÓXIMOS PASOS DESPUÉS DE INSTALAR")
    print("=" * 50)
    print("1. Verificar instalación: psql --version")
    print("2. Configurar .env: python configurar_postgresql.py")
    print("3. Verificar sistema: python verificar_sistema.py")
    print("4. Migrar a PostgreSQL: python migrate_to_postgresql.py")

if __name__ == "__main__":
    main()







