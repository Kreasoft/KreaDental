#!/usr/bin/env python
"""
Script para resetear la contraseña de PostgreSQL
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

def mostrar_instrucciones_reset():
    """Mostrar instrucciones para resetear contraseña"""
    print("🔐 INSTRUCCIONES PARA RESETEAR CONTRASEÑA DE POSTGRESQL")
    print("=" * 60)
    print()
    print("OPCIÓN 1: Usar pgAdmin (Recomendado)")
    print("-" * 40)
    print("1. Abrir pgAdmin")
    print("2. Conectar al servidor PostgreSQL")
    print("3. Click derecho en 'Login/Group Roles'")
    print("4. Seleccionar 'postgres'")
    print("5. Ir a la pestaña 'Definition'")
    print("6. Cambiar la contraseña")
    print("7. Guardar cambios")
    print()
    print("OPCIÓN 2: Usar línea de comandos")
    print("-" * 40)
    print("1. Abrir Command Prompt como Administrador")
    print("2. Ejecutar: psql -U postgres")
    print("3. Si pide contraseña, presionar Enter (puede estar vacía)")
    print("4. Ejecutar: ALTER USER postgres PASSWORD 'nueva_contraseña';")
    print("5. Ejecutar: \\q para salir")
    print()
    print("OPCIÓN 3: Resetear desde archivo de configuración")
    print("-" * 40)
    print("1. Detener servicio de PostgreSQL")
    print("2. Crear archivo temporal con:")
    print("   ALTER USER postgres PASSWORD 'nueva_contraseña';")
    print("3. Ejecutar: psql -U postgres -f archivo_temporal.sql")
    print("4. Iniciar servicio de PostgreSQL")
    print()

def probar_contrasenas_comunes():
    """Probar contraseñas comunes"""
    print("🔍 PROBANDO CONTRASEÑAS COMUNES")
    print("=" * 40)
    
    contrasenas = [
        "postgres",
        "postgres123",
        "admin",
        "password",
        "123456",
        "root",
        "postgresql",
        "kreasoft",
        "kreadental",
        "",
    ]
    
    for i, password in enumerate(contrasenas, 1):
        print(f"{i:2d}. Probando: {'(vacía)' if password == '' else password}")
        
        try:
            env = os.environ.copy()
            if password:
                env['PGPASSWORD'] = password
            
            result = subprocess.run([
                'psql', '-U', 'postgres', '-d', 'postgres',
                '-c', 'SELECT 1;'
            ], capture_output=True, text=True, env=env)
            
            if result.returncode == 0:
                print(f"   ✅ ¡FUNCIONA! Contraseña: {password if password else '(vacía)'}")
                return password
            else:
                print(f"   ❌ No funciona")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n❌ Ninguna contraseña común funcionó")
    return None

def configurar_autenticacion_trust():
    """Configurar autenticación trust (sin contraseña)"""
    print("🔧 CONFIGURANDO AUTENTICACIÓN TRUST")
    print("=" * 40)
    
    # Ruta del archivo pg_hba.conf
    pg_hba_path = "C:\\Program Files\\PostgreSQL\\17\\data\\pg_hba.conf"
    
    if not os.path.exists(pg_hba_path):
        print(f"❌ No se encontró pg_hba.conf en: {pg_hba_path}")
        print("   Busca el archivo en tu instalación de PostgreSQL")
        return False
    
    print(f"✅ Archivo encontrado: {pg_hba.conf}")
    print("\n📝 INSTRUCCIONES MANUALES:")
    print("1. Abrir el archivo pg_hba.conf como Administrador")
    print("2. Buscar la línea que contiene:")
    print("   local   all             postgres                                md5")
    print("3. Cambiar 'md5' por 'trust':")
    print("   local   all             postgres                                trust")
    print("4. Guardar el archivo")
    print("5. Reiniciar el servicio de PostgreSQL")
    print("6. Probar conexión sin contraseña")
    
    return True

def crear_script_reset():
    """Crear script para resetear contraseña"""
    print("📝 CREANDO SCRIPT DE RESET")
    print("=" * 30)
    
    script_content = """@echo off
echo Reseteando contraseña de PostgreSQL...
echo.

REM Detener servicio
net stop postgresql-x64-17
echo Servicio detenido

REM Crear archivo temporal con comando SQL
echo ALTER USER postgres PASSWORD 'postgres123'; > reset_password.sql

REM Ejecutar comando SQL
psql -U postgres -d postgres -f reset_password.sql

REM Limpiar archivo temporal
del reset_password.sql

REM Iniciar servicio
net start postgresql-x64-17
echo Servicio iniciado

echo.
echo Contraseña reseteada a: postgres123
echo.
pause
"""
    
    try:
        with open('reset_postgresql_password.bat', 'w') as f:
            f.write(script_content)
        print("✅ Script creado: reset_postgresql_password.bat")
        print("   Ejecuta este archivo como Administrador")
        return True
    except Exception as e:
        print(f"❌ Error creando script: {e}")
        return False

def main():
    print("🔐 RESETEADOR DE CONTRASEÑA DE POSTGRESQL")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Configurar PATH
    if not configurar_path():
        print("❌ No se pudo configurar PATH de PostgreSQL")
        return
    
    # Mostrar opciones
    print("\n📋 OPCIONES DISPONIBLES:")
    print("1. Probar contraseñas comunes")
    print("2. Configurar autenticación sin contraseña")
    print("3. Crear script de reset")
    print("4. Ver instrucciones detalladas")
    
    opcion = input("\nSelecciona una opción (1-4): ").strip()
    
    if opcion == "1":
        contrasena = probar_contrasenas_comunes()
        if contrasena is not None:
            print(f"\n🎉 ¡Contraseña encontrada: {contrasena if contrasena else '(vacía)'}!")
            print("   Puedes continuar con la migración")
        else:
            print("\n❌ No se encontró contraseña válida")
    
    elif opcion == "2":
        configurar_autenticacion_trust()
    
    elif opcion == "3":
        crear_script_reset()
    
    elif opcion == "4":
        mostrar_instrucciones_reset()
    
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    main()


"""
Script para resetear la contraseña de PostgreSQL
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

def mostrar_instrucciones_reset():
    """Mostrar instrucciones para resetear contraseña"""
    print("🔐 INSTRUCCIONES PARA RESETEAR CONTRASEÑA DE POSTGRESQL")
    print("=" * 60)
    print()
    print("OPCIÓN 1: Usar pgAdmin (Recomendado)")
    print("-" * 40)
    print("1. Abrir pgAdmin")
    print("2. Conectar al servidor PostgreSQL")
    print("3. Click derecho en 'Login/Group Roles'")
    print("4. Seleccionar 'postgres'")
    print("5. Ir a la pestaña 'Definition'")
    print("6. Cambiar la contraseña")
    print("7. Guardar cambios")
    print()
    print("OPCIÓN 2: Usar línea de comandos")
    print("-" * 40)
    print("1. Abrir Command Prompt como Administrador")
    print("2. Ejecutar: psql -U postgres")
    print("3. Si pide contraseña, presionar Enter (puede estar vacía)")
    print("4. Ejecutar: ALTER USER postgres PASSWORD 'nueva_contraseña';")
    print("5. Ejecutar: \\q para salir")
    print()
    print("OPCIÓN 3: Resetear desde archivo de configuración")
    print("-" * 40)
    print("1. Detener servicio de PostgreSQL")
    print("2. Crear archivo temporal con:")
    print("   ALTER USER postgres PASSWORD 'nueva_contraseña';")
    print("3. Ejecutar: psql -U postgres -f archivo_temporal.sql")
    print("4. Iniciar servicio de PostgreSQL")
    print()

def probar_contrasenas_comunes():
    """Probar contraseñas comunes"""
    print("🔍 PROBANDO CONTRASEÑAS COMUNES")
    print("=" * 40)
    
    contrasenas = [
        "postgres",
        "postgres123",
        "admin",
        "password",
        "123456",
        "root",
        "postgresql",
        "kreasoft",
        "kreadental",
        "",
    ]
    
    for i, password in enumerate(contrasenas, 1):
        print(f"{i:2d}. Probando: {'(vacía)' if password == '' else password}")
        
        try:
            env = os.environ.copy()
            if password:
                env['PGPASSWORD'] = password
            
            result = subprocess.run([
                'psql', '-U', 'postgres', '-d', 'postgres',
                '-c', 'SELECT 1;'
            ], capture_output=True, text=True, env=env)
            
            if result.returncode == 0:
                print(f"   ✅ ¡FUNCIONA! Contraseña: {password if password else '(vacía)'}")
                return password
            else:
                print(f"   ❌ No funciona")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n❌ Ninguna contraseña común funcionó")
    return None

def configurar_autenticacion_trust():
    """Configurar autenticación trust (sin contraseña)"""
    print("🔧 CONFIGURANDO AUTENTICACIÓN TRUST")
    print("=" * 40)
    
    # Ruta del archivo pg_hba.conf
    pg_hba_path = "C:\\Program Files\\PostgreSQL\\17\\data\\pg_hba.conf"
    
    if not os.path.exists(pg_hba_path):
        print(f"❌ No se encontró pg_hba.conf en: {pg_hba_path}")
        print("   Busca el archivo en tu instalación de PostgreSQL")
        return False
    
    print(f"✅ Archivo encontrado: {pg_hba.conf}")
    print("\n📝 INSTRUCCIONES MANUALES:")
    print("1. Abrir el archivo pg_hba.conf como Administrador")
    print("2. Buscar la línea que contiene:")
    print("   local   all             postgres                                md5")
    print("3. Cambiar 'md5' por 'trust':")
    print("   local   all             postgres                                trust")
    print("4. Guardar el archivo")
    print("5. Reiniciar el servicio de PostgreSQL")
    print("6. Probar conexión sin contraseña")
    
    return True

def crear_script_reset():
    """Crear script para resetear contraseña"""
    print("📝 CREANDO SCRIPT DE RESET")
    print("=" * 30)
    
    script_content = """@echo off
echo Reseteando contraseña de PostgreSQL...
echo.

REM Detener servicio
net stop postgresql-x64-17
echo Servicio detenido

REM Crear archivo temporal con comando SQL
echo ALTER USER postgres PASSWORD 'postgres123'; > reset_password.sql

REM Ejecutar comando SQL
psql -U postgres -d postgres -f reset_password.sql

REM Limpiar archivo temporal
del reset_password.sql

REM Iniciar servicio
net start postgresql-x64-17
echo Servicio iniciado

echo.
echo Contraseña reseteada a: postgres123
echo.
pause
"""
    
    try:
        with open('reset_postgresql_password.bat', 'w') as f:
            f.write(script_content)
        print("✅ Script creado: reset_postgresql_password.bat")
        print("   Ejecuta este archivo como Administrador")
        return True
    except Exception as e:
        print(f"❌ Error creando script: {e}")
        return False

def main():
    print("🔐 RESETEADOR DE CONTRASEÑA DE POSTGRESQL")
    print("=" * 50)
    print("KreaDental Cloud - Sistema de Gestión Dental")
    print("=" * 50)
    
    # Configurar PATH
    if not configurar_path():
        print("❌ No se pudo configurar PATH de PostgreSQL")
        return
    
    # Mostrar opciones
    print("\n📋 OPCIONES DISPONIBLES:")
    print("1. Probar contraseñas comunes")
    print("2. Configurar autenticación sin contraseña")
    print("3. Crear script de reset")
    print("4. Ver instrucciones detalladas")
    
    opcion = input("\nSelecciona una opción (1-4): ").strip()
    
    if opcion == "1":
        contrasena = probar_contrasenas_comunes()
        if contrasena is not None:
            print(f"\n🎉 ¡Contraseña encontrada: {contrasena if contrasena else '(vacía)'}!")
            print("   Puedes continuar con la migración")
        else:
            print("\n❌ No se encontró contraseña válida")
    
    elif opcion == "2":
        configurar_autenticacion_trust()
    
    elif opcion == "3":
        crear_script_reset()
    
    elif opcion == "4":
        mostrar_instrucciones_reset()
    
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    main()





