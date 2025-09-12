#!/usr/bin/env python
"""
Script para crear respaldo de la base de datos SQLite
"""

import os
import shutil
from datetime import datetime

def crear_respaldo():
    """Crear respaldo de la base de datos SQLite"""
    
    # Verificar que existe la base de datos
    if not os.path.exists('db.sqlite3'):
        print("❌ No se encontró el archivo db.sqlite3")
        return False
    
    # Crear directorio de respaldos si no existe
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Generar nombre del archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"db_backup_{timestamp}.sqlite3"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Copiar la base de datos
        shutil.copy2('db.sqlite3', backup_path)
        print(f"✅ Respaldo creado exitosamente: {backup_path}")
        
        # Mostrar información del archivo
        file_size = os.path.getsize(backup_path)
        print(f"   📁 Tamaño: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear respaldo: {e}")
        return False

def listar_respaldos():
    """Listar respaldos existentes"""
    
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        print("📁 No hay respaldos disponibles")
        return
    
    print("📁 Respaldos disponibles:")
    print("-" * 40)
    
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.startswith('db_backup_') and filename.endswith('.sqlite3'):
            file_path = os.path.join(backup_dir, filename)
            file_size = os.path.getsize(file_path)
            file_time = os.path.getmtime(file_path)
            backups.append((filename, file_size, file_time))
    
    # Ordenar por fecha (más reciente primero)
    backups.sort(key=lambda x: x[2], reverse=True)
    
    for filename, file_size, file_time in backups:
        date_str = datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"   {filename} ({file_size:,} bytes) - {date_str}")

def main():
    """Función principal"""
    print("💾 Creando respaldo de la base de datos SQLite")
    print("=" * 50)
    
    # Crear respaldo
    if crear_respaldo():
        print("\n📋 Lista de respaldos:")
        listar_respaldos()
        print("\n✅ Respaldo completado exitosamente")
        print("   Ahora puedes proceder con la migración a PostgreSQL")
    else:
        print("\n❌ Error al crear respaldo")

if __name__ == "__main__":
    main()


"""
Script para crear respaldo de la base de datos SQLite
"""

import os
import shutil
from datetime import datetime

def crear_respaldo():
    """Crear respaldo de la base de datos SQLite"""
    
    # Verificar que existe la base de datos
    if not os.path.exists('db.sqlite3'):
        print("❌ No se encontró el archivo db.sqlite3")
        return False
    
    # Crear directorio de respaldos si no existe
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Generar nombre del archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"db_backup_{timestamp}.sqlite3"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Copiar la base de datos
        shutil.copy2('db.sqlite3', backup_path)
        print(f"✅ Respaldo creado exitosamente: {backup_path}")
        
        # Mostrar información del archivo
        file_size = os.path.getsize(backup_path)
        print(f"   📁 Tamaño: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear respaldo: {e}")
        return False

def listar_respaldos():
    """Listar respaldos existentes"""
    
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        print("📁 No hay respaldos disponibles")
        return
    
    print("📁 Respaldos disponibles:")
    print("-" * 40)
    
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.startswith('db_backup_') and filename.endswith('.sqlite3'):
            file_path = os.path.join(backup_dir, filename)
            file_size = os.path.getsize(file_path)
            file_time = os.path.getmtime(file_path)
            backups.append((filename, file_size, file_time))
    
    # Ordenar por fecha (más reciente primero)
    backups.sort(key=lambda x: x[2], reverse=True)
    
    for filename, file_size, file_time in backups:
        date_str = datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
        print(f"   {filename} ({file_size:,} bytes) - {date_str}")

def main():
    """Función principal"""
    print("💾 Creando respaldo de la base de datos SQLite")
    print("=" * 50)
    
    # Crear respaldo
    if crear_respaldo():
        print("\n📋 Lista de respaldos:")
        listar_respaldos()
        print("\n✅ Respaldo completado exitosamente")
        print("   Ahora puedes proceder con la migración a PostgreSQL")
    else:
        print("\n❌ Error al crear respaldo")

if __name__ == "__main__":
    main()





