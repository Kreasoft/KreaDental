#!/usr/bin/env python
"""
Script para convertir archivo de UTF-16 a UTF-8
"""

def convertir_archivo():
    """Convertir archivo de UTF-16 a UTF-8"""
    try:
        # Leer archivo en UTF-16
        with open('datos_completos_sqlite.json', 'r', encoding='utf-16') as f:
            content = f.read()
        
        # Escribir archivo en UTF-8
        with open('datos_completos_sqlite.json', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Archivo convertido de UTF-16 a UTF-8")
        return True
        
    except Exception as e:
        print(f"❌ Error convirtiendo archivo: {e}")
        return False

if __name__ == "__main__":
    convertir_archivo()

Script para convertir archivo de UTF-16 a UTF-8
"""

def convertir_archivo():
    """Convertir archivo de UTF-16 a UTF-8"""
    try:
        # Leer archivo en UTF-16
        with open('datos_completos_sqlite.json', 'r', encoding='utf-16') as f:
            content = f.read()
        
        # Escribir archivo en UTF-8
        with open('datos_completos_sqlite.json', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Archivo convertido de UTF-16 a UTF-8")
        return True
        
    except Exception as e:
        print(f"❌ Error convirtiendo archivo: {e}")
        return False

if __name__ == "__main__":
    convertir_archivo()
